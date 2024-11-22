import asyncio
import sys

import aiofiles
from scholarly import scholarly


async def write_paper_to_file(paper, file):
    """Write a single paper entry to the markdown file."""
    row = (
        f"| {paper['title']} | {paper['authors']} | "
        f"{paper['year']} | {paper['citations']} | "
        f"[Link]({paper['link']}) |\n"
    )
    await file.write(row)


async def init_markdown_file():
    """Initialize the markdown file with headers."""
    async with aiofiles.open("papers.md", "w", encoding="utf-8") as f:
        await f.write("# LLM for Security 相关文章\n\n")
        await f.write("| 标题 | 作者 | 年份 | 引用次数 | 链接 |\n")
        await f.write("| ---- | ---- | ---- | -------- | ---- |\n")


async def process_paper(pub, outfile):
    """Process a single paper and write it to file."""
    try:
        paper = {
            "title": pub["bib"].get("title", "N/A"),
            "authors": ", ".join(pub["bib"].get("author", ["N/A"])),
            "year": pub["bib"].get("pub_year", "N/A"),
            "citations": pub.get("num_citations", "N/A"),
            "link": pub.get("pub_url") or pub.get("eprint_url", "N/A"),
        }
        await write_paper_to_file(paper, outfile)
        print(f"Processed: {paper['title']}")
    except Exception as e:
        print(f"Error processing paper: {e}", file=sys.stderr)


async def fetch_papers(query):
    """Fetch papers and stream results to file."""
    await init_markdown_file()

    search_query = scholarly.search_pubs(query)
    async with aiofiles.open("papers.md", "a", encoding="utf-8") as f:
        while True:
            try:
                pub = next(search_query)
                await process_paper(pub, f)
                await f.flush()  # Ensure immediate writing to disk
            except StopIteration:
                print("No more papers found", file=sys.stderr)
                break
            except Exception as e:
                print(f"Error fetching paper: {e}", file=sys.stderr)
                continue


async def main():
    query = "LLM for Security"
    await fetch_papers(query)


if __name__ == "__main__":
    asyncio.run(main())
