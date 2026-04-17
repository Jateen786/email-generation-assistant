# Email Generation Assistant — AI Engineer Assessment

A production-ready email generation assistant with a custom evaluation framework comparing two LLMs.

---

## Project Structure

```
email-assistant/
├── src/
│   ├── assistant.py      # Email generator (Role-Playing + Few-Shot prompting)
│   ├── metrics.py        # 3 custom evaluation metrics
│   └── evaluate.py       # Full evaluation pipeline (runs both models)
├── data/
│   └── scenarios.py      # 10 test scenarios + human reference emails
├── outputs/              # Generated CSVs, JSONs (created on run)
└── README.md
```

---

## Setup

```bash
git clone <your-repo-url>
cd email-assistant
pip install groq
export GROQ_API_KEY=your_key_here   # Get free key at console.groq.com
```

---

## Running the Evaluation

```bash
python src/evaluate.py
```

Outputs to `outputs/`:
- `evaluation_results.csv` — raw scores for all 10 scenarios × 2 models
- `evaluation_results.json` — full detail including metric breakdowns
- `summary.json` — average scores per model

---

## Advanced Prompting Technique

**Technique: Role-Playing + Few-Shot Examples (combined)**

**Why this combination?**

- **Role-Playing** ("You are Alexandra Chen, a Fortune-500 communications specialist...") anchors the model's persona and sets consistent quality expectations. It reduces variance in style and register.
- **Few-Shot Examples** provide concrete input→output demonstrations. For email generation — a task with a clear structural template — showing 2 worked examples dramatically improves fact integration, opening quality, and closing decisiveness.
- **Combined effect**: Role-Playing sets *who* is writing; Few-Shot shows *how* they write. Together they outperform either technique alone.

---

## Custom Evaluation Metrics

### Metric 1: Fact Recall Rate (0–10)
**Definition**: Measures whether all required key facts were naturally included in the generated email.

**Logic**: LLM-as-a-Judge (claude-haiku-4-5) evaluates each fact individually, allowing for paraphrasing. Score = (facts present / total facts) × 10.

**Why**: Pure string matching fails when the model paraphrases correctly. LLM judgment captures semantic presence.

---

### Metric 2: Tone Accuracy Score (0–10)
**Definition**: Measures how closely the email's tone matches the requested tone descriptor.

**Logic**: LLM-as-a-Judge rates 4 sub-dimensions (Word Choice, Sentence Structure, Opening Line, Closing) each out of 2.5, summed to 10.

**Why**: Tone is multi-dimensional. Evaluating sub-components gives a granular failure signal (e.g., "word choice is right but the closing is too casual").

---

### Metric 3: Conciseness Score (0–10)
**Definition**: Measures whether the email is appropriately concise and information-dense.

**Logic**: Hybrid automated metric combining:
- **Length score** (4 pts): Ideal 80–180 words = full marks; scaled penalties for longer emails
- **Information density** (3 pts): Key fact mentions per sentence ratio
- **Filler phrase penalty** (3 pts): Deducts for clichés like "circle back", "touch base", "synergy"

**Why**: LLM-generated emails tend toward verbosity. This metric penalises padding while rewarding efficient fact delivery.

---

## Model Comparison

| Metric | llama-3.3-70b-versatile | llama-3.1-8b-instant |
|--------|:-----------------------:|:--------------------:|
| Fact Recall | — | — |
| Tone Accuracy | — | — |
| Conciseness | — | — |
| **Overall Avg** | — | — |

*(Scores populated after running `evaluate.py`)*

**Recommendation**: See `outputs/summary.json` for data-driven recommendation after running the evaluation.

---

## Interactive UI

The project also ships as a React artifact (see `email_assistant.jsx`) that runs the full pipeline in-browser via the Anthropic API, with:
- Live email generation interface
- One-click evaluation runner with progress tracking
- Results table with per-scenario drill-down
- Auto-generated comparative analysis report
- CSV + JSON export
