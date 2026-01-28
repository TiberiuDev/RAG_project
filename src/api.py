from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .rag_pipeline import build_store_from_csv_safe, simple_answer_pipeline


app = FastAPI()

# Allow CORS for frontend (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store = build_store_from_csv_safe()

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AskResponse)
async def ask_endpoint(request: AskRequest):
    answer = simple_answer_pipeline(request.question, vector_store)
    return {"answer": answer}
