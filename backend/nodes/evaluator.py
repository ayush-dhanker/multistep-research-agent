from langchain_groq import ChatGroq
from state import ResearchState
import os

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


def evaluator_node(state: ResearchState) -> dict:
    topic = state["topic"]
    results = "\n\n".join(state['results'])

    response = llm.invoke(f"""
                          You are a research evaluator.
        
        Topic: {topic}
        
        Research collected:
        {results}
        
        Do two things:
        1. Write a concise 150-200 word summary answering the topic
        2. Score the quality of this summary from 0.0 to 1.0
           based on: coverage, clarity, and factual depth
        
        Respond in this exact format:
        SUMMARY: <your summary here>
        SCORE: <number between 0.0 and 1.0>             
                          """)

    content = response.content.strip()

    # parse summary
    summary_line = [l for l in content.split(
        "\n") if l.startswith("SUMMARY:")][0]
    summary = summary_line.replace("SUMMARY:", "").strip()

    # parse score
    score_line = [l for l in content.split("\n") if l.startswith("SCORE:")][0]
    score = float(score_line.replace("SCORE:", "").strip())

    return {
        "output": summary,
        "quality_score": score,
        "iteration_count": state["iteration_count"] + 1
    }
