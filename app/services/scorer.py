from __future__ import annotations

import json
import re

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import Settings
from app.models.schemas import CandidateResult

_SYSTEM_PROMPT = (
    "You are a recruiting assistant. Given a job description, a resume, and a "
    "similarity score, return a JSON object with keys: "
    '"name" (candidate name extracted from resume), '
    '"score" (float 0-1, your adjusted relevance score), '
    '"explanation" (2-3 sentence summary of fit), '
    '"skill_gaps" (list of missing skills). '
    "Return ONLY valid JSON, no markdown."
)


def _parse_llm_json(raw: str) -> dict:
    """Robustly parse JSON from LLM output, stripping markdown fences if present."""
    raw = raw.strip()
    # Strip ```json ... ``` or ``` ... ``` fences that LLMs sometimes add despite instructions
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw.strip())


class ScoringService:
    """Calls the LLM via LangChain to produce an explanation (SRP).

    Receives a pre-computed similarity score — does NOT depend on EmbeddingService
    (Interface Segregation).
    """

    def __init__(self, settings: Settings) -> None:
        self._llm = ChatGoogleGenerativeAI(
            model=settings.chat_model,
            google_api_key=settings.google_api_key,
            temperature=0.3,
        )

    def explain_match(
        self,
        jd_text: str,
        resume_text: str,
        similarity_score: float,
    ) -> CandidateResult:
        user_msg = (
            f"Job Description:\n{jd_text}\n\n"
            f"Resume:\n{resume_text}\n\n"
            f"Cosine similarity score: {similarity_score:.4f}"
        )
        messages = [
            ("system", _SYSTEM_PROMPT),
            ("human", user_msg),
        ]
        response = self._llm.invoke(messages)
        raw = response.content or "{}"
        data = _parse_llm_json(raw)
        return CandidateResult(**data)

    async def aexplain_match(
        self,
        jd_text: str,
        resume_text: str,
        similarity_score: float,
    ) -> CandidateResult:
        user_msg = (
            f"Job Description:\n{jd_text}\n\n"
            f"Resume:\n{resume_text}\n\n"
            f"Cosine similarity score: {similarity_score:.4f}"
        )
        messages = [
            ("system", _SYSTEM_PROMPT),
            ("human", user_msg),
        ]
        response = await self._llm.ainvoke(messages)
        raw = response.content or "{}"
        data = _parse_llm_json(raw)
        return CandidateResult(**data)