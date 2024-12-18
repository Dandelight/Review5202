import asyncio
import os
from pathlib import Path

import aiofiles
import anthropic
from tqdm import tqdm


class DocumentSummarizer:

    def __init__(
        self,
        input_dir: str = "markdown/pypdf",
        output_dir: str = "summaries",
        api_key: str | None = None,
    ):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize Claude client
        self.client = anthropic.AsyncAnthropic(
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY")
        )

        # Load system prompt from file
        prompt_path = Path("Thinking-Claude/model_instructions/v4-20241118.md")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        except Exception as e:
            print(f"Error loading system prompt from {prompt_path}: {e}")
            raise

    async def read_markdown(self, file_path: Path) -> str:
        """Read content from markdown file."""
        try:
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                return await f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""

    async def save_summary(self, summary: str, output_path: Path) -> bool:
        """Save summary to file."""
        try:
            async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
                await f.write(summary)
            return True
        except Exception as e:
            print(f"Error saving summary to {output_path}: {e}")
            return False

    async def summarize_document(self, content: str) -> str:
        """Generate summary using Claude API."""
        try:
            message = await self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=4096,
                temperature=0.3,
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Please summarize this research paper:\n\n{content}",
                    }
                ],
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error during summarization: {e}")
            return ""

    async def process_single_document(self, file_path: Path):
        """Process a single document."""
        try:
            # Read content
            content = await self.read_markdown(file_path)
            if not content:
                return False

            # Generate summary
            summary = await self.summarize_document(content)
            if not summary:
                return False

            # Save summary
            output_path = self.output_dir / f"{file_path.stem}_summary.md"
            return await self.save_summary(summary, output_path)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False

    async def process_all_documents(self):
        """Process all markdown documents in the input directory concurrently."""
        markdown_files = list(self.input_dir.glob("*.md"))

        if not markdown_files:
            print(f"No markdown files found in {self.input_dir}")
            return

        # Create tasks for all documents
        tasks = [
            self.process_single_document(file_path) for file_path in markdown_files
        ]

        # Process all documents concurrently with progress bar
        with tqdm(total=len(markdown_files), desc="Summarizing documents") as pbar:
            results = await asyncio.gather(*tasks)
            for file_path, success in zip(markdown_files, results):
                if success:
                    print(f"Successfully summarized: {file_path.name}")
                else:
                    print(f"Failed to summarize: {file_path.name}")
                pbar.update(1)

    async def generate_index(self):
        """Generate an index file of all summaries."""
        summary_files = list(self.output_dir.glob("*_summary.md"))

        if not summary_files:
            return

        index_content = "# Paper Summaries Index\n\n"

        for file_path in sorted(summary_files):
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                content = await f.read()
                # Extract title from summary (assuming it's the first line)
                title = content.split("\n")[0].strip("# ")
                index_content += f"- [{title}](./{file_path.name})\n"

        await self.save_summary(index_content, self.output_dir / "index.md")


async def main():
    # Initialize summarizer with configurable batch size
    summarizer = DocumentSummarizer()

    # Process all documents concurrently
    await summarizer.process_all_documents()

    # Generate index
    await summarizer.generate_index()


if __name__ == "__main__":
    asyncio.run(main())
