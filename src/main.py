import asyncio
from pathlib import Path

from chains.paper_collection import PaperCollectionChain
from chains.summarization import SummarizationChain
from chains.text_extraction import TextExtractionChain
from config.settings import settings


async def main():
    # Initialize chains
    paper_chain = PaperCollectionChain()
    extraction_chain = TextExtractionChain()
    summary_chain = SummarizationChain()

    # Create necessary directories
    for dir in [settings.PAPERS_DIR, settings.MARKDOWN_DIR, settings.SUMMARIES_DIR]:
        dir.mkdir(parents=True, exist_ok=True)

    # Run the pipeline
    papers = await paper_chain.run("LLM for Security")
    for paper in papers:
        # Download and process each paper
        # Extract text
        # Generate summary
        pass


if __name__ == "__main__":
    asyncio.run(main())
