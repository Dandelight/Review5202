import asyncio
import json
import os
import subprocess
from pathlib import Path
from typing import Literal

import aiofiles
import PyPDF2
from tqdm import tqdm


class PDFExtractor:
    def __init__(self, input_dir: str = "papers", output_dir: str = "markdown"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Create subdirectories for each extractor
        self.pypdf_dir = self.output_dir / "pypdf"
        self.nougat_dir = self.output_dir / "nougat"
        self.pypdf_dir.mkdir(exist_ok=True)
        self.nougat_dir.mkdir(exist_ok=True)

    async def extract_with_pypdf(self, pdf_path: Path) -> str | None:
        """Extract text using PyPDF2."""
        try:
            text = []
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text.append(page.extract_text())

            return "\n\n".join(text)
        except Exception as e:
            print(f"Error extracting text from {pdf_path} with PyPDF2: {e}")
            return None

    async def extract_with_nougat(self, pdf_path: Path) -> str:
        """Extract text using Nougat."""
        try:
            output_path = self.nougat_dir / f"{pdf_path.stem}_nougat.mmd"

            # Run nougat-ocr command
            process = await asyncio.create_subprocess_exec(
                "nougat",
                str(pdf_path),
                "--out",
                str(self.nougat_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            await process.communicate()

            # Read the generated markdown file
            if output_path.exists():
                async with aiofiles.open(output_path, "r", encoding="utf-8") as f:
                    return await f.read()
            return ""

        except Exception as e:
            print(f"Error extracting text from {pdf_path} with Nougat: {e}")
            return ""

    async def save_markdown(self, content: str, output_path: Path) -> bool:
        """Save extracted text as markdown. Returns True if successful."""
        try:
            # Skip empty or whitespace-only content
            if not content or not content.strip():
                return False

            async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
                await f.write(content)
            return True
        except Exception as e:
            print(f"Error saving markdown to {output_path}: {e}")
            return False

    async def process_single_pdf(
        self, pdf_path: Path, extractor: Literal["pypdf", "nougat", "both"] = "both"
    ):
        """Process a single PDF file with specified extractor(s)."""
        results = []

        if extractor in ["pypdf", "both"]:
            pypdf_output = self.pypdf_dir / f"{pdf_path.stem}_pypdf.md"
            text = await self.extract_with_pypdf(pdf_path)
            if text:  # Only save if we got content
                success = await self.save_markdown(text, pypdf_output)
                if not success:
                    print(f"Skipping empty PyPDF2 output for {pdf_path.name}")

        if extractor in ["nougat", "both"]:
            nougat_output = self.nougat_dir / f"{pdf_path.stem}_nougat.md"
            text = await self.extract_with_nougat(pdf_path)
            if text:  # Only save if we got content
                success = await self.save_markdown(text, nougat_output)
                if not success:
                    print(f"Skipping empty Nougat output for {pdf_path.name}")

    async def process_all_pdfs(
        self, extractor: Literal["pypdf", "nougat", "both"] = "both"
    ):
        """Process all PDFs in the input directory."""
        pdf_files = list(self.input_dir.glob("*.pdf"))

        with tqdm(total=len(pdf_files), desc="Processing PDFs") as pbar:
            for pdf_path in pdf_files:
                await self.process_single_pdf(pdf_path, extractor)
                pbar.update(1)

    async def generate_comparison_report(self):
        """Generate a comparison report of the extractions."""
        report = []
        pypdf_files = set(
            f.stem.replace("_pypdf", "") for f in self.pypdf_dir.glob("*.md")
        )
        nougat_files = set(
            f.stem.replace("_nougat", "") for f in self.nougat_dir.glob("*.md")
        )

        all_files = sorted(pypdf_files | nougat_files)

        for base_name in all_files:
            pypdf_path = self.pypdf_dir / f"{base_name}_pypdf.md"
            nougat_path = self.nougat_dir / f"{base_name}_nougat.md"

            comparison = {
                "filename": base_name,
                "pypdf_exists": pypdf_path.exists(),
                "nougat_exists": nougat_path.exists(),
                "pypdf_size": pypdf_path.stat().st_size if pypdf_path.exists() else 0,
                "nougat_size": (
                    nougat_path.stat().st_size if nougat_path.exists() else 0
                ),
            }
            report.append(comparison)

        # Save comparison report
        async with aiofiles.open(self.output_dir / "comparison_report.json", "w") as f:
            await f.write(json.dumps(report, indent=2))


async def main():
    extractor = PDFExtractor()

    # Process PDFs with both extractors
    await extractor.process_all_pdfs(extractor="pypdf")

    # Generate comparison report
    await extractor.generate_comparison_report()


if __name__ == "__main__":
    asyncio.run(main())
