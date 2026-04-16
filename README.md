# Multistep Research Agent

> Give it a topic. It researches, evaluates, and refines until the answer is good enough.

A LangGraph-based agentic pipeline that takes a user topic, breaks it into sub-queries, fetches from multiple sources in parallel, evaluates output quality, and iteratively refines until a quality threshold is met — using all 4 core agentic workflow patterns.

---

## Demo

```
Input:  "quantum computing"

→ Planner    generates 3 focused sub-queries
→ Fetcher    searches all 3 in parallel via Tavily
→ Evaluator  scores output quality (0.0 – 1.0)
→ Refiner    improves if score < 0.8 (max 3 iterations)
→ Output     clean research summary
```

---

## Architecture

```
START → planner → [fetcher × N] → evaluator → END
                                       ↑          ↓
                                    refiner ←  score < 0.8
```

| Pattern | Where used | LangGraph mechanism |
|---|---|---|
| Sequential | planner → fetcher → evaluator → refiner | `add_edge` |
| Parallel | fetch N sources simultaneously | `Send()` API |
| Conditional | good enough or refine? | `add_conditional_edges` |
| Iterative | loop until threshold met | cycle back to evaluator |

---

## Project Structure

```
backend/
├── state.py          # shared TypedDict state
├── graph.py          # LangGraph graph wiring
├── main.py           # entry point
└── nodes/
    ├── planner.py    # LLM breaks topic into sub-queries
    ├── fetcher.py    # Tavily web search (parallel)
    ├── evaluator.py  # LLM scores + writes draft output
    ├── refiner.py    # LLM improves weak output
    └── router.py     # conditional edge logic
```

---

## Tech Stack

- **LangGraph** — agentic graph orchestration
- **LangChain + Groq** — LLM calls (llama-3.3-70b-versatile, free tier)
- **Tavily** — web search API (free tier)
- **Python 3.12**

---

## Setup

```bash
# clone and enter backend
git clone https://github.com/your-username/multistep-research-agent
cd multistep-research-agent/backend

# create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# install dependencies
pip install langgraph langchain-groq tavily-python python-dotenv

# set environment variables
cp .env.example .env
# add your GROQ_API_KEY and TAVILY_API_KEY
```

**.env**
```
GROQ_API_KEY=your-groq-key
TAVILY_API_KEY=your-tavily-key
```

Get free keys:
- Groq: https://console.groq.com
- Tavily: https://tavily.com

---

## Run

```bash
python main.py
```

**Example output:**
```
Steps: ['what is quantum computing', 'real world uses', 'limitations 2024']
Score: 0.8
Iterations: 1

Output:
Quantum computing leverages superposition and entanglement to solve
problems exponentially faster than classical computers...
```

---

## State Schema

Every node reads from and writes to a shared `ResearchState`:

```python
class ResearchState(TypedDict):
    topic: str                                    # user input
    step: str                                     # single query per fetcher worker
    steps: List[str]                              # sub-queries from planner
    results: Annotated[List[str], operator.add]   # merged fetch results
    output: str                                   # current draft answer
    quality_score: float                          # evaluator score 0.0–1.0
    iteration_count: int                          # loop counter
```

---

## Design Decisions & Critical Thinking

### Why `Send()` over fixed parallel edges?

Fixed edges (`add_edge("planner", "fetcher_1")` × 3) require knowing the number of branches at build time. The planner dynamically decides how many sub-queries to generate — could be 2, 3, or 5. `Send()` handles this at runtime, spawning exactly as many workers as there are steps. Fixed edges would break if the planner returned 4 queries instead of 3.

### Why `Annotated[List[str], operator.add]` on results?

When 3 fetcher instances run in parallel and each returns `{"results": [content]}`, LangGraph needs to know how to merge them. Without `operator.add`, the last fetcher overwrites the previous two — you lose data silently. The reducer tells LangGraph to append all lists together before passing state to the next node.

### What if the Tavily API goes down mid-run?

The current implementation has no retry logic — a failed fetch returns an empty string and the evaluator scores low, triggering the refiner unnecessarily. A production fix would wrap `client.search()` in a try/except with exponential backoff, and skip failed queries gracefully rather than passing empty strings downstream.

### Can a user exploit the iterative loop to run indefinitely?

Yes, if `iteration_count` check is removed from the router. The hard exit at 3 iterations prevents infinite loops, but a malicious or confusing topic could still consume 3 full LLM + search cycles before exiting. A production fix would add per-request cost tracking and a timeout at the graph level.

### Why does the evaluator write the draft output, not the refiner?

The evaluator produces the first draft as a side effect of scoring — it needs to understand the content to score it, so writing the summary costs no extra LLM call. The refiner then improves this existing draft. If the evaluator only scored and the refiner wrote from scratch each time, you'd pay for an extra LLM call every iteration.

### What would you improve next?

Structured output parsing. Currently `ast.literal_eval()` on the planner and string splitting on the evaluator are fragile — if the LLM adds preamble text, both crash. Replacing these with LangChain's `with_structured_output()` and Pydantic models would make parsing robust and remove the need for prompt engineering around output format.

---

## What I learned

- How LangGraph's `Send()` API enables dynamic parallel dispatch at runtime
- The difference between `add_edge` fan-out (fixed branches) and `Send()` (runtime branches)
- How `Annotated` reducers solve the fan-in merge problem cleanly
- Why state design matters — every node's behaviour depends on getting state right first
- How to design explicit exit conditions for iterative loops in production systems

---

## License

MIT