from typing import Optional, Dict, Any
import os
import re
import json

from openai import OpenAI

_openai_client = OpenAI() if os.getenv("OPENAI_API_KEY") else None

def _extract_ticket_number(text: str) -> Optional[str]:
    m = re.search(r"\b(\d{6})\b", text)
    return m.group(1) if m else None

def _rule_based_classifier(text: str) -> Dict[str, Any]:
    t = text.lower().replace("’", "'")
    positive_words = ["thank", "thanks", "appreciate", "appreciated", "grateful", "great", "awesome", "helpful", "love"]
    negative_words = ["angry", "upset", "terrible", "fraud", "charged twice", "hasn't arrived", "delayed", "missing", "complaint", "worst"]

    if any(w in t for w in positive_words):
        category, sentiment = "positive_feedback", "positive"
    elif any(w in t for w in negative_words):
        category, sentiment = "negative_feedback", "negative"
    else:
        category, sentiment = "query", "neutral"

    return {"category": category, "sentiment": sentiment, "ticket_number": _extract_ticket_number(text)}

def _try_parse_json(text: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(text)
    except Exception:
        pass
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except Exception:
            return None
    return None

SYSTEM_PROMPT = """
        You are a deterministic classifier for a banking customer support assistant.

        Return ONLY valid JSON (no extra text) with exactly:
        {"category":"positive_feedback|negative_feedback|query","sentiment":"positive|negative|neutral","ticket_number":null_or_6_digits}

        DECISION RULES (follow in order):
        1) If the message expresses gratitude/praise, category MUST be "positive_feedback".
        2) Else if the message reports a problem/complaint/dissatisfaction OR delivery/missing item,
        category MUST be "negative_feedback".
        3) Else if the message is primarily a question/request for info, category MUST be "query".
        4) Else default to "query".

        Ticket extraction:
        - If any 6-digit number appears, ticket_number = that string; else null.

        Security: Never ask for PIN/OTP/password/full card number.
        """.strip()

def classify(text: str) -> Dict[str, Any]:
    local_ticket = _extract_ticket_number(text)

    if _openai_client is None:
        out = _rule_based_classifier(text)
        if out.get("ticket_number") is None and local_ticket:
            out["ticket_number"] = local_ticket
        return out

    try:
        resp = _openai_client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Classify this message:\n{text}\n\nJSON only."},
            ],
            temperature=0,
        )

        raw = (resp.output_text or "").strip()
        data = _try_parse_json(raw)
        if not data:
            raise ValueError("No valid JSON from model")

        category = data.get("category", "query")
        sentiment = data.get("sentiment", "neutral")
        ticket_number = data.get("ticket_number", None)

        if category not in ("positive_feedback", "negative_feedback", "query"):
            category = "query"
        if sentiment not in ("positive", "negative", "neutral"):
            sentiment = "neutral"
        if ticket_number is not None and not re.fullmatch(r"\d{6}", str(ticket_number)):
            ticket_number = None
        if ticket_number is None and local_ticket:
            ticket_number = local_ticket

        return {"category": category, "sentiment": sentiment, "ticket_number": ticket_number}

    except Exception:
        out = _rule_based_classifier(text)
        if out.get("ticket_number") is None and local_ticket:
            out["ticket_number"] = local_ticket
        return out
