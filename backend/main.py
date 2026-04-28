from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from database import init_db, save_post, get_recent_posts, review_post

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


class TextRequest(BaseModel):
    text: str


class ReviewRequest(BaseModel):
    reviewer: str


@app.post("/analyze-text")
def analyze(request: TextRequest):
    text = request.text

    # -------- Language Detection --------
    try:
        language = detect(text)
    except LangDetectException:
        language = "unknown"

    # -------- Simple Scoring Logic (Demo AI) --------
    credibility_score = 60
    panic_index = 20
    location = "Hyderabad"

    if credibility_score > 80:
        status = "Auto Verified"
        action = "No Action"
    elif credibility_score > 50:
        status = "Under Review"
        action = "Human Review Required"
    else:
        status = "Likely Fake"
        action = "Suppress"

    # -------- Save To Database --------
    save_post(
        text,
        credibility_score,
        status,
        action,
        location,
        panic_index
    )

    return {
        "status": status,
        "credibility_score": credibility_score,
        "panic_index": panic_index,
        "location": location,
        "response_action": action,
        "language": language
    }


@app.get("/recent-posts")
def recent_posts():
    return get_recent_posts()


@app.post("/approve/{post_id}")
def approve(post_id: int, review: ReviewRequest):
    review_post(
        post_id,
        review.reviewer,
        "Verified by Authority",
        "Manually Approved"
    )
    return {"message": "Post approved"}


@app.post("/reject/{post_id}")
def reject(post_id: int, review: ReviewRequest):
    review_post(
        post_id,
        review.reviewer,
        "Rejected by Authority",
        "Marked as Misinformation"
    )
    return {"message": "Post rejected"}