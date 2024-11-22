import asyncio
import os
import re
from pathlib import Path
from urllib.parse import urlparse

import aiofiles
import aiohttp
from tqdm import tqdm

DOWNLOAD_DIR = "papers"
MAX_CONCURRENT_DOWNLOADS = 5  # Limit concurrent downloads to avoid rate limiting
TIMEOUT = aiohttp.ClientTimeout(total=60)  # 60 second timeout


async def sanitize_filename(title):
    """Create a safe filename from the paper title."""
    # Remove invalid characters and limit length
    safe_title = re.sub(r"[^\w\s-]", "", title)
    safe_title = re.sub(r"\s+", "_", safe_title.strip())
    return safe_title[:100]  # Limit filename length


async def download_paper(session, title, url, semaphore, progress_bar):
    """Download a single paper with rate limiting."""
    async with semaphore:
        try:
            # Skip if URL is invalid or N/A
            if url == "N/A" or not url.startswith(("http://", "https://")):
                progress_bar.update(1)
                return False

            # Create safe filename
            safe_title = await sanitize_filename(title)

            # Determine file extension based on URL or default to .pdf
            parsed_url = urlparse(url)
            ext = os.path.splitext(parsed_url.path)[1] or ".pdf"
            filename = f"{safe_title}{ext}"
            filepath = os.path.join(DOWNLOAD_DIR, filename)

            # Skip if file already exists
            if os.path.exists(filepath):
                progress_bar.update(1)
                return True

            async with session.get(url, timeout=TIMEOUT) as response:
                if response.status == 200:
                    async with aiofiles.open(filepath, "wb") as f:
                        await f.write(await response.read())
                    progress_bar.update(1)
                    return True
                else:
                    print(f"\nFailed to download {title}: HTTP {response.status}")
                    progress_bar.update(1)
                    return False

        except Exception as e:
            print(f"\nError downloading {title}: {str(e)}")
            progress_bar.update(1)
            return False


async def parse_markdown_and_download():
    """Parse the markdown file and download all papers."""
    # Create download directory if it doesn't exist
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Read and parse markdown file
    papers = []
    async with aiofiles.open("papers.md", "r", encoding="utf-8") as f:
        content = await f.read()

    # Parse markdown table rows
    pattern = r"\|(.*?)\|(.*?)\|(.*?)\|\s*(\d*)\s*\|\s*\[Link\]\((.*?)\)\s*\|"
    matches = re.finditer(pattern, content)

    for match in matches:
        title = match.group(1).strip()
        url = match.group(5).strip()
        if title and url:  # Skip empty entries
            papers.append((title, url))

    # Set up async download with rate limiting
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)
    async with aiohttp.ClientSession() as session:
        with tqdm(total=len(papers), desc="Downloading papers") as progress_bar:
            tasks = [
                download_paper(session, title, url, semaphore, progress_bar)
                for title, url in papers
            ]
            results = await asyncio.gather(*tasks)

    # Print summary
    successful = sum(1 for r in results if r)
    print(
        f"\nDownload complete: {successful}/{len(papers)} papers downloaded successfully"
    )


async def main():
    await parse_markdown_and_download()


if __name__ == "__main__":
    asyncio.run(main())
