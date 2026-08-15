from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import evaluate, improve

# Creates tables if they don't exist yet — fine for a solo project,
# use Alembic migrations if this grows into a team project
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Prompt Evaluator + Improver API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://prompt-forging.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(evaluate.router)
app.include_router(improve.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "prompt-evaluator-api"}
