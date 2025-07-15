from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
import sys
import importlib.util
from dotenv import load_dotenv
load_dotenv()

# Use environment variable for frontend URL in production
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")

# Dynamically import the cointelegraph module
cointelegraph_path = os.path.join(os.path.dirname(__file__), "cointelegraph.py")
spec = importlib.util.spec_from_file_location("cointelegraph", cointelegraph_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Could not load spec for {cointelegraph_path}")
cointelegraph = importlib.util.module_from_spec(spec)
sys.modules["cointelegraph"] = cointelegraph
spec.loader.exec_module(cointelegraph)

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://newaiagent.onrender.com"],  # For development, allow all. For production, use your frontend URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    topic: Optional[str] = None
    keywords: Optional[List[str]] = None
    article_type: Optional[str] = None  # e.g., "news", "report"
    length: Optional[int] = None

@app.post("/generate")
async def generate_article(req: GenerateRequest):
    html_file = cointelegraph.run_ultimate_agent()
    article_html = ""
    if html_file and os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            article_html = f.read()
    return {
        "html_file": html_file,
        "article_html": article_html
    }

@app.get("/logs", response_class=PlainTextResponse)
async def get_logs():
    log_file = "app.log"
    if not os.path.exists(log_file):
        return ""
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()[-50:]
    return "".join(lines)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
