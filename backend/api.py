from graph import build_graph
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # local dev
        "http://localhost:3000",   # docker
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = build_graph()


class ResearchRequest(BaseModel):
    topic: str


class ResearchResponse(BaseModel):
    topic: str
    output: str
    quality_score: float
    iteration_count: int
    steps: list[str]


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/research", response_model=ResearchResponse)
def run_research(request: ResearchRequest):
    result = agent.invoke({
        "topic": request.topic,
        "step": "",
        "steps": [],
        "results": [],
        "output": "",
        "quality_score": 0.0,
        "iteration_count": 0
    })

    return ResearchResponse(
        topic=request.topic,
        output=result["output"],
        quality_score=result["quality_score"],
        iteration_count=result["iteration_count"],
        steps=result["steps"]
    )
