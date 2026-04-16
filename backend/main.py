from graph import build_graph
from dotenv import load_dotenv
load_dotenv()


agent = build_graph()

result = agent.invoke({
    "topic": "quantum computing",
    "step": "",
    "steps": [],
    "results": [],
    "output": "",
    "quality_score": 0.0,
    "iteration_count": 0
})

print(f"Score: {result['quality_score']}")
print(f"Iterations: {result['iteration_count']}")
print(f"\nOutput:\n{result['output']}")
