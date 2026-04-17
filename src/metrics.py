"""
3 Custom Evaluation Metrics for Email Generation Quality

Metric 1: Fact Recall Rate       — Did the email include all required key facts?
Metric 2: Tone Accuracy Score    — Does the email match the requested tone? (LLM-as-Judge)
Metric 3: Conciseness Score      — Is the email appropriately concise? (word count + density)
"""

import json
import re
from groq import Groq

client = Groq()  # reads GROQ_API_KEY from environment
JUDGE_MODEL = "llama-3.1-8b-instant"  # fast cheap model for evaluation


# ── METRIC 1: Fact Recall Rate ────────────────────────────────────────────────
# Logic: Use LLM to check if each key fact is present in the generated email.
# Score = (facts found / total facts) * 10
# Range: 0–10

def metric_fact_recall(generated_email: str, key_facts: list[str]) -> dict:
    """
    Measures whether all key facts are present in the generated email.
    Uses LLM-as-a-Judge to handle paraphrasing (not just exact match).
    """
    facts_str = "\n".join(f"{i+1}. {f}" for i, f in enumerate(key_facts))
    
    prompt = f"""You are an evaluator checking if an email includes required facts.

EMAIL:
{generated_email}

REQUIRED FACTS:
{facts_str}

For each fact, determine if it is clearly communicated in the email (exact wording not required — paraphrasing counts).

Respond ONLY with valid JSON, no markdown:
{{
  "results": [
    {{"fact": "...", "present": true/false, "evidence": "brief quote or 'not found'"}}
  ]
}}"""

    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=500,
    )
    
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    
    data = json.loads(raw)
    facts_found = sum(1 for r in data["results"] if r["present"])
    score = round((facts_found / len(key_facts)) * 10, 2)
    
    return {
        "score": score,
        "facts_found": facts_found,
        "total_facts": len(key_facts),
        "details": data["results"]
    }


# ── METRIC 2: Tone Accuracy Score ─────────────────────────────────────────────
# Logic: LLM-as-a-Judge rates how well the email matches the requested tone.
# Judges across 4 sub-dimensions: word choice, sentence structure, opening, closing.
# Score: 0–10

def metric_tone_accuracy(generated_email: str, requested_tone: str) -> dict:
    """
    Measures how accurately the email reflects the requested tone.
    LLM judges across 4 tone sub-dimensions.
    """
    prompt = f"""You are a professional communications expert evaluating tone accuracy in emails.

REQUESTED TONE: {requested_tone}

EMAIL:
{generated_email}

Rate how well this email matches the requested tone across these 4 dimensions (each 0–2.5):
1. Word Choice: vocabulary fits the tone
2. Sentence Structure: length/complexity fits the tone  
3. Opening Line: sets the right tone immediately
4. Closing: ends with appropriate tone

Respond ONLY with valid JSON, no markdown:
{{
  "word_choice": {{\"score\": 0.0, \"reason\": \"...\"}},
  "sentence_structure": {{\"score\": 0.0, \"reason\": \"...\"}},
  "opening_line": {{\"score\": 0.0, \"reason\": \"...\"}},
  "closing": {{\"score\": 0.0, \"reason\": \"...\"}}
}}"""

    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=500,
    )
    
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    
    data = json.loads(raw)
    total = sum(v["score"] for v in data.values())
    score = round(min(total, 10), 2)
    
    return {
        "score": score,
        "breakdown": data
    }


# ── METRIC 3: Conciseness Score ───────────────────────────────────────────────
# Logic: Hybrid automated metric.
#   - Word count penalty: emails over 200 words lose points
#   - Information density: unique key fact mentions per sentence
#   - No filler phrase detection (penalises clichés)
# Score: 0–10

FILLER_PHRASES = [
    "i hope this email finds you well",
    "i hope you are doing well",
    "please do not hesitate",
    "as per my last email",
    "going forward",
    "at the end of the day",
    "touch base",
    "circle back",
    "synergy",
    "bandwidth",
]

def metric_conciseness(generated_email: str, key_facts: list[str]) -> dict:
    """
    Measures if the email is concise and information-dense.
    Penalises excessive length and filler phrases.
    """
    body = generated_email.lower()
    words = generated_email.split()
    word_count = len(words)
    sentences = [s.strip() for s in re.split(r'[.!?]', generated_email) if len(s.strip()) > 10]
    sentence_count = max(len(sentences), 1)
    
    # Sub-score 1: Word count (ideal: 80–180 words = full marks)
    if word_count <= 180:
        length_score = 4.0
    elif word_count <= 250:
        length_score = 3.0
    elif word_count <= 320:
        length_score = 2.0
    else:
        length_score = 1.0
    
    # Sub-score 2: Information density (facts per sentence, max 3pts)
    fact_mentions = sum(
        1 for fact in key_facts
        if any(word.lower() in body for word in fact.split() if len(word) > 4)
    )
    density = fact_mentions / sentence_count
    density_score = min(density * 6, 3.0)
    
    # Sub-score 3: Filler phrase penalty (max 3pts, -0.75 per filler found)
    fillers_found = [p for p in FILLER_PHRASES if p in body]
    filler_score = max(3.0 - (len(fillers_found) * 0.75), 0)
    
    total = round(length_score + density_score + filler_score, 2)
    
    return {
        "score": min(total, 10),
        "word_count": word_count,
        "length_score": length_score,
        "density_score": round(density_score, 2),
        "filler_score": filler_score,
        "fillers_found": fillers_found
    }
