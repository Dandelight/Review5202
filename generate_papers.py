from scholarly import ProxyGenerator, scholarly


def fetch_papers(query, num_papers=10):
    papers = []
    search_query = scholarly.search_pubs(query)
    for _ in range(num_papers):
        try:
            pub = next(search_query)
            print(pub)
            paper = {
                "title": pub.bib.get("title", "N/A"),
                "authors": ", ".join(pub.bib.get("author", ["N/A"])),
                "year": pub.bib.get("year", "N/A"),
                "citations": pub.citedby if hasattr(pub, "citedby") else "N/A",
                "link": pub.bib.get("url", "N/A"),
            }
            papers.append(paper)
        except StopIteration:
            break
        except Exception as e:
            print(f"Error fetching paper: {e}")
            continue
    return papers


def generate_markdown(papers):
    with open("papers.md", "w", encoding="utf-8") as f:
        f.write("# LLM for Security 相关文章\n\n")
        f.write("| 标题 | 作者 | 年份 | 引用次数 | 链接 |\n")
        f.write("| ---- | ---- | ---- | -------- | ---- |\n")
        for paper in papers:
            f.write(
                f"| {paper['title']} | {paper['authors']} | {paper['year']} | {paper['citations']} | [{paper['link']}]({paper['link']}) |\n"
            )


if __name__ == "__main__":
    query = "LLM for Security"
    papers = fetch_papers(query, num_papers=10)
    generate_markdown(papers)
