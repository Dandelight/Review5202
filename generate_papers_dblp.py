import logging
import sys

sys.path.append("dblp-api")

import dblp

logging.basicConfig(level=logging.INFO)


def fetch_papers(query: str, max_results: int = 100) -> list:
    try:
        results = dblp.search([query])
        return results
    except Exception as e:
        logging.error(f"An error occurred while fetching papers: {e}")
        return []


def generate_markdown(papers: list, filename: str = "papers.md") -> None:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# LLM for Security 相关文章\n\n")
            f.write("| 标题 | 作者 | 年份 | 期刊/会议 | URL | DOI |\n")
            f.write("| ---- | ---- | ---- | --------- | ---- | ---- |\n")
            for paper in papers:
                title = paper.get("title", "N/A")
                authors = paper.get("authors", "N/A")
                year = paper.get("year", "N/A")
                venue = paper.get("venue", "N/A")
                url = paper.get("url", "N/A")
                doi = paper.get("doi", "N/A")
                f.write(
                    f"| {title} | {authors} | {year} | {venue} | [{url}]({url}) | [{doi}]({doi}) |\n"
                )
    except Exception as e:
        logging.error(f"An error occurred while generating Markdown: {e}")


if __name__ == "__main__":
    query = "Large Language Models Security"
    papers = fetch_papers(query)
    generate_markdown(papers)
