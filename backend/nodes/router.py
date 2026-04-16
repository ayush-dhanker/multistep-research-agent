from state import ResearchState
from langgraph.graph import END


def route_after_evaluator(state: ResearchState) -> str:
    if state["quality_score"] >= 0.8:
        return END
    elif state["iteration_count"] >= 3:
        return END        # max retries hit, exit anyway
    else:
        return "refiner"
