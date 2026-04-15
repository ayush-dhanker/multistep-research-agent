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

print(f"Steps: {result['steps']}")
print(f"\nFetched {len(result['results'])} results")
for i, r in enumerate(result['results']):
    print(f"\n--- Result {i+1} ---\n{r[:200]}...")
