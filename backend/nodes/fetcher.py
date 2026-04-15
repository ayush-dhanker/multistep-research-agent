from tavily import TavilyClient
from state import ResearchState
import os

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def fetcher_node(state: ResearchState) -> dict:
    query = state["step"]

    response = client.search(
        query=query,
        max_results=3
    )

    # combining top results into 0ne string
    content = "\n\n".join([
        r["content"] for r in response["results"]
    ])

    return {"results": [content]}
