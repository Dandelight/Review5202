import asyncio
from typing import Dict, List

from langchain.tools import Tool
from scholarly import scholarly


class ScholarlyClient:
    @staticmethod
    async def search_papers(query: str, limit: int = None) -> List[Dict]:
        search_query = scholarly.search_pubs(query)
        papers = []

        while True:
            try:
                pub = next(search_query)
                paper = {
                    "title": pub.bib.get("title", "N/A"),
                    "authors": pub.bib.get("author", ["N/A"]),
                    "year": pub.bib.get("pub_year", "N/A"),
                    "citations": pub.get("num_citations", "N/A"),
                    "url": pub.get("pub_url") or pub.get("eprint_url", "N/A"),
                }
                papers.append(paper)

                if limit and len(papers) >= limit:
                    break
            except StopIteration:
                break

        return papers

    def get_tool(self) -> Tool:
        return Tool(
            name="ScholarlySearch",
            func=self.search_papers,
            description="Search for academic papers using Google Scholar",
        )
