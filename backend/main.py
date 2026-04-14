from graph import build_graph
from dotenv import load_dotenv

load_dotenv()

agent = build_graph()


result = agent.invoke({
    "topic": "quantum computing",
    "steps": [],
    "results": [],
    "output": "",
    "quality_score": 0.0,
    "iteration_count": 0
})


print("Steps generated:")
for step in result["steps"]:
    print(f"  - {step}")
