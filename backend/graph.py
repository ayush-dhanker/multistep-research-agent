from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from state import ResearchState
from nodes.planner import planner_node
from nodes.fetcher import fetcher_node


def route_to_fetchers(state: ResearchState):
    return [Send("fetcher", {"step": s}) for s in state["steps"]]


def build_graph():
    graph = StateGraph(ResearchState)

    # adding nodes-- functions/task
    graph.add_node("planner", planner_node)
    graph.add_node("fetcher", fetcher_node)

    # adding edges - what runs next
    graph.add_edge(START, "planner")
    graph.add_conditional_edges("planner", route_to_fetchers, ["fetcher"])
    graph.add_edge("fetcher", END)  # step - 2

    return graph.compile()
