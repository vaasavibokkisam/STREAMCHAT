import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from llm import stream_chat

app = FastAPI(title="StreamChat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_start_time = time.time()


# ---------- Schemas ----------

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []  # [{role: "user"|"assistant", content: "..."}]


class ResetRequest(BaseModel):
    session_id: str


# ---------- Endpoints ----------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "uptime_seconds": round(time.time() - _start_time, 2),
        "model": "llama-3.3-70b-versatile",  # ✅ updated to Groq model
    }


@app.post("/chat")
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message must not be empty")

    return StreamingResponse(
        stream_chat(req.message, req.history),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # disables nginx buffering
        },
    )


@app.post("/reset")
async def reset(req: ResetRequest):
    if not req.session_id:
        raise HTTPException(status_code=400, detail="session_id is required")
    return {"status": "ok", "session_id": req.session_id, "message": "Session reset confirmed"}