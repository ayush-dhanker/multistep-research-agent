from langchain_groq import ChatGroq
from state import ResearchState
import ast

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


def planner_node(state: ResearchState) -> dict:
    topic = state["topic"]

    response = llm.invoke(f"""
        You are a research planner.
        Break this topic into exactly 3 specific search queries: "{topic}"
        
        Return ONLY a Python list of 3 strings, nothing else.
        Example: ["query one", "query two", "query three"]                          
                          """)

    steps = ast.literal_eval(response.content.strip())

    return {"steps": steps}
