from typing import List, Optional, Dict, Any
from langgraph.graph import StateGraph, END
import requests
from bs4 import BeautifulSoup
import re
from pydantic import BaseModel


class ResearchState(BaseModel):
    urls: List[str]
    gathered_info: Optional[List[str]] = None
    final_answer: Optional[str] = None


def crawl_website(url, max_paragraphs=5):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all('p')
        content = "\n".join(p.text for p in paragraphs[:max_paragraphs])
        return content
    except Exception as e:
        return f"Error crawling {url}: {e}"


def research_agent(state: ResearchState) -> ResearchState:
    urls = state.urls
    gathered_info = []

    print("\n[Research Agent] Crawling websites...\n")

    for url in urls:
        content = crawl_website(url)
        gathered_info.append(content)
    
    return ResearchState(
        urls=urls,
        gathered_info=gathered_info
    )


def drafting_agent(state: ResearchState) -> ResearchState:
    gathered_info = state.gathered_info or []

    print("\n[Drafting Agent] Drafting summary...\n")

    full_text = "\n".join(gathered_info)
    full_text = re.sub(r'\s+', ' ', full_text)

    if len(full_text) > 1000:
        draft = full_text[:1000] + "..."
    else:
        draft = full_text

    return ResearchState(
        urls=state.urls,
        gathered_info=state.gathered_info,
        final_answer=f"Drafted Summary:\n{draft}"
    )


def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("ResearchAgent", research_agent)
    graph.add_node("DraftingAgent", drafting_agent)

    graph.set_entry_point("ResearchAgent")
    graph.add_edge("ResearchAgent", "DraftingAgent")
    graph.add_edge("DraftingAgent", END)

    return graph.compile()

def main():
    urls = input("Enter website URLs separated by commas:\n").split(',')
    urls = [url.strip() for url in urls if url.strip()]

    if not urls:
        print("No URLs provided. Exiting...")
        return

    graph = build_graph()

    initial_state = ResearchState(urls=urls, research_results=[], final_answer=None)

    result = graph.invoke(initial_state)

    print("\nFinal Output:\n")
    print(result['final_answer'])

if __name__ == "__main__":
    main()
