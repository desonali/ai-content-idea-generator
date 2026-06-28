"""
AI Content Idea Generator - Backend
------------------------------------
A small FastAPI service that generates short-form video/content ideas
for a given topic using the Groq API (free tier, no card required).
"""

import os
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = FastAPI(title="AI Content Idea Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


class IdeaRequest(BaseModel):
    topic: str
    count: int = 5


class IdeaResponse(BaseModel):
    ideas: List[str]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/generate-ideas", response_model=IdeaResponse)
def generate_ideas(request: IdeaRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic must not be empty.")

    if not client:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not set. Add it to your .env file.",
        )

    prompt = (
        f"Generate {request.count} short-form video content ideas "
        f"(TikTok/Reels/Shorts style) about the topic: '{request.topic}'. "
        "Each idea should be one punchy sentence. Return only a numbered list, "
        "no intro or outro text."
    )

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        )
        text = completion.choices[0].message.content
        ideas = [
            line.split(".", 1)[-1].strip(" -")
            for line in text.strip().split("\n")
            if line.strip()
        ]
        return IdeaResponse(ideas=ideas[: request.count])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
