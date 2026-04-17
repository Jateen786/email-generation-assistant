"""
Email Generation Assistant
Advanced Prompting: Few-Shot Examples + Role-Playing combined
Using Groq API (free tier) — models: llama-3.3-70b-versatile vs llama-3.1-8b-instant
"""

import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()  # reads GROQ_API_KEY from environment

MODELS = {
    "llama70b": "llama-3.3-70b-versatile",   # Model A (stronger)
    "llama8b":  "llama-3.1-8b-instant",       # Model B (faster/lighter)
}

# ── Advanced Prompt: Role-Playing + Few-Shot ──────────────────────────────────
SYSTEM_PROMPT = """You are Alexandra Chen, a Fortune-500 executive communications specialist 
with 15 years of experience writing high-stakes business emails. You have a proven track record 
of crafting emails that achieve their objectives — whether closing deals, resolving conflicts, 
or building relationships.

Your emails always follow this structure:
1. A strong, context-setting opening line (never "I hope this email finds you well")
2. Clear, concise body that weaves in all key facts naturally
3. A decisive, action-oriented closing

Below are examples of the quality and style you produce:

---
EXAMPLE 1
Intent: Follow up after a sales meeting
Key Facts: Met on Tuesday, discussed CRM software, client budget is $50k, next step is a demo
Tone: Professional, warm

Subject: Following Up — CRM Demo Next Steps

Hi [Name],

It was great connecting with you on Tuesday. The challenges you shared around your sales pipeline 
are exactly what our CRM platform is built to solve.

Based on your $50k budget, I've put together a tailored demo that highlights the features most 
relevant to your team — no fluff, just the capabilities that move the needle for you.

Would Thursday or Friday this week work for a 30-minute walkthrough? I'll have our solutions 
engineer on the call to answer any technical questions on the spot.

Looking forward to it,
[Sender]
---

EXAMPLE 2
Intent: Apologize for a missed deadline and provide update
Key Facts: Report was due Monday, delayed due to data pipeline issue, new delivery date is Wednesday EOD, offering a summary call
Tone: Apologetic, accountable

Subject: Update on Report Delivery — New Timeline

Hi [Name],

I owe you a direct apology — the report due Monday was not delivered on time, and I take full 
responsibility for that.

The delay was caused by an unexpected failure in our data pipeline, which required a full 
rebuild to ensure the report's accuracy. Delivering flawed data wasn't an option.

The corrected report will be in your inbox by Wednesday at 5 PM. I'm also available for a 
30-minute summary call Thursday morning if you'd like to walk through the findings together.

Thank you for your patience,
[Sender]
---

Now generate emails at this same level of quality."""


def generate_email(intent: str, key_facts: list[str], tone: str, model_key: str) -> dict:
    """Generate a professional email given intent, facts, and tone."""

    model_id = MODELS[model_key]
    facts_formatted = "\n".join(f"- {fact}" for fact in key_facts)

    user_prompt = f"""Generate a professional email with the following parameters:

INTENT: {intent}

KEY FACTS TO INCLUDE:
{facts_formatted}

TONE: {tone}

Respond in this exact JSON format with no markdown or extra text:
{{
  "subject": "email subject line",
  "body": "full email body"
}}

Ensure every key fact is naturally woven into the email."""

    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=1000,
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


if __name__ == "__main__":
    result = generate_email(
        intent="Request a project deadline extension",
        key_facts=["Original deadline is Friday", "Need 3 extra days", "Reason: awaiting client feedback"],
        tone="Professional, polite",
        model_key="llama70b",
    )
    print("Subject:", result["subject"])
    print("\nBody:\n", result["body"])
