from langchain_groq import ChatGroq
from state import ResearchState

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


def refiner_node(state: ResearchState) -> dict:
    topic = state["topic"]
    current_output = state["output"]
    current_score = state["quality_score"]

    response = llm.invoke(f"""
         You are a research refiner.
        
        Topic: {topic}
        Current score: {current_score}/1.0
        
        Current summary that needs improvement:
        {current_output}
        
        Rewrite this summary to improve:
        - Coverage of the topic
        - Clarity of explanation
        - Factual depth
        
        Return ONLY the improved summary, nothing else.  
    """)

    return {
        "output": response.content.strip()
    }
