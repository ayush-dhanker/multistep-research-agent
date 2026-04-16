from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from state import ResearchState
from nodes.planner import planner_node
from nodes.fetcher import fetcher_node
from nodes.evaluator import evaluator_node
from nodes.refiner import refiner_node
from nodes.router import route_after_evaluator


def route_to_fetchers(state: ResearchState):
    return [Send("fetcher", {"step": s}) for s in state["steps"]]


def build_graph():
    graph = StateGraph(ResearchState)

    # adding nodes-- functions/task
    graph.add_node("planner", planner_node)
    graph.add_node("fetcher", fetcher_node)
    graph.add_node("evaluator", evaluator_node)
    graph.add_node("refiner", refiner_node)

    # adding edges - what runs next
    graph.add_edge(START, "planner")
    graph.add_conditional_edges("planner", route_to_fetchers, ["fetcher"])
    graph.add_edge("fetcher", 'evaluator')
    graph.add_conditional_edges(
        "evaluator", route_after_evaluator, ["refiner", END])
    graph.add_edge("refiner", "evaluator")
    return graph.compile()
