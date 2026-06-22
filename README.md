##StreamChat##

A real-time AI chat application with token-by-token streaming via Server-Sent Events (SSE).


Project Structure

streamchat/
├── backend/
│   ├── main.py          # FastAPI app — /chat, /health, /reset
│   ├── llm.py           # Groq LLM streaming + context trimming
│   ├── requirements.txt # Python dependencies
│   └── .env             # API keys (not committed to GitHub)
├── frontend/
│   └── index.html       # Vanilla JS SSE consumer UI
├── tests/
│   └── test_api.py      # pytest test suite
└── README.md


Tech Stack

LayerTechnologyBackendFastAPI + UvicornLLMGroq API (llama-3.3-70b-versatile)StreamingServer-Sent Events (SSE)FrontendVanilla HTML + CSS + JavaScriptDeploymentRender (backend) + Netlify (frontend)


Live Demo


##Frontend: https://harmonious-hamster-d21947.netlify.app##
##Backend: https://streamchat-n03f.onrender.com##



Local Setup

1. Clone the repository

bashgit clone https://github.com/vaasavibokkisam/STREAMCHAT.git
cd STREAMCHAT

2. Create virtual environment

bashpython -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

3. Install dependencies

bashcd backend
pip install -r requirements.txt

4. Set up API key

Create a .env file inside the backend/ folder:

GROQ_API_KEY=your_groq_api_key_here

Get a free key from: https://console.groq.com/keys

5. Start the backend

bashcd backend
uvicorn main:app --reload --port 8000

Verify it's running:

http://localhost:8000/health

6. Start the frontend

Open a new terminal:

bashcd frontend
python -m http.server 3000

Open browser:

http://localhost:3000


API Reference

POST /chat

Streams LLM response token by token via SSE.

Request:

json{
  "message": "What is RAG?",
  "history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"}
  ]
}

Response: text/event-stream

data: Retrieval

data: -Augmented

data: Generation...

event: token_usage
data: 142

event: done
data: [DONE]

GET /health

Returns service status. Responds within 200ms.

Response:

json{
  "status": "ok",
  "uptime_seconds": 10.5,
  "model": "llama-3.3-70b-versatile"
}

POST /reset

Resets a session (stateless — confirms reset).

Request:

json{ "session_id": "abc-123" }

Response:

json{
  "status": "ok",
  "session_id": "abc-123",
  "message": "Session reset confirmed"
}


Running Tests

bashpip install pytest httpx
pytest tests/test_api.py -v

Expected output:

PASSED tests/test_api.py::test_health_returns_ok
PASSED tests/test_api.py::test_health_responds_fast
PASSED tests/test_api.py::test_reset_returns_session_id
PASSED tests/test_api.py::test_reset_requires_session_id
PASSED tests/test_api.py::test_chat_rejects_empty_message


Features


Token-by-token streaming via SSE
Typing indicator while waiting for first token
Multi-turn conversation history
Context window trimming (drops oldest messages when history > 8000 tokens)
Token usage counter in UI header
Error handling for connection failures
Stateless API — client sends full history each request
CORS enabled for cross-origin frontend requests



Why SSE over WebSockets?

SSE is a better fit for LLM streaming because the communication is unidirectional — the server pushes tokens to the client, and the client has nothing to send back mid-stream.

SSEWebSocketsDirectionServer → Client onlyBidirectionalProtocolPlain HTTPUpgrade handshake requiredProxy supportWorks out of the boxNeeds extra configBrowser supportNative EventSource APINative but more complexComplexitySimpleHigher overhead

WebSockets add bidirectional complexity (connection management, ping/pong, reconnection logic) that this use case simply doesn't need. SSE is simpler, lighter, and perfectly suited for streaming LLM responses.


Deployment

Backend — Render


Connect GitHub repo to Render
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Add environment variable: GROQ_API_KEY


Frontend — Netlify


Drag and drop frontend/ folder to https://app.netlify.com/drop
Instant deployment, no config needed
