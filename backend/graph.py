from langgraph.graph import StateGraph, START, END
from state import ResearchState
from nodes.planner import planner_node


def build_graph():
    graph = StateGraph(ResearchState)

    # adding nodes-- functions/task
    graph.add_node("planner", planner_node)

    # adding edges - what runs next
    graph.add_edge(START, "planner")
    graph.add_edge("planner", END)  # step - 1

    return graph.compile()
