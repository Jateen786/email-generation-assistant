"""
Main Evaluation Pipeline
Runs 10 scenarios × 2 models, scores with 3 custom metrics, outputs CSV + JSON report
"""

import sys
import os
import csv
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.assistant import generate_email
from src.metrics import metric_fact_recall, metric_tone_accuracy, metric_conciseness
from data.scenarios import SCENARIOS

MODELS = {
    "llama70b": "llama-3.3-70b-versatile",
    "llama8b":  "llama-3.1-8b-instant",
}

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def evaluate_scenario(scenario: dict, model_key: str) -> dict:
    print(f"  → Generating email (model={model_key})...")
    try:
        email = generate_email(
            intent=scenario["intent"],
            key_facts=scenario["key_facts"],
            tone=scenario["tone"],
            model_key=model_key,
        )
    except Exception as e:
        print(f"    ✗ Generation failed: {e}")
        return None

    full_text = f"Subject: {email['subject']}\n\n{email['body']}"
    
    print(f"  → Scoring metrics...")
    
    try:
        m1 = metric_fact_recall(full_text, scenario["key_facts"])
    except Exception as e:
        print(f"    ✗ Metric 1 failed: {e}")
        m1 = {"score": 0, "facts_found": 0, "total_facts": len(scenario["key_facts"])}

    try:
        m2 = metric_tone_accuracy(full_text, scenario["tone"])
    except Exception as e:
        print(f"    ✗ Metric 2 failed: {e}")
        m2 = {"score": 0}

    try:
        m3 = metric_conciseness(full_text, scenario["key_facts"])
    except Exception as e:
        print(f"    ✗ Metric 3 failed: {e}")
        m3 = {"score": 0, "word_count": 0}

    avg = round((m1["score"] + m2["score"] + m3["score"]) / 3, 2)

    return {
        "scenario_id": scenario["id"],
        "intent": scenario["intent"],
        "tone": scenario["tone"],
        "model": model_key,
        "generated_subject": email["subject"],
        "generated_body": email["body"],
        # Metric scores
        "m1_fact_recall": m1["score"],
        "m1_facts_found": m1.get("facts_found", "-"),
        "m1_total_facts": m1.get("total_facts", "-"),
        "m2_tone_accuracy": m2["score"],
        "m3_conciseness": m3["score"],
        "m3_word_count": m3.get("word_count", "-"),
        "overall_avg": avg,
        # Full detail blobs
        "m1_detail": m1,
        "m2_detail": m2,
        "m3_detail": m3,
    }


def run_evaluation():
    print("\n" + "="*60)
    print("  EMAIL ASSISTANT EVALUATION PIPELINE")
    print("="*60)
    
    all_results = []

    for model_key in MODELS:
        print(f"\n▶ Model: {model_key} ({MODELS[model_key]})")
        print("-" * 50)
        for scenario in SCENARIOS:
            print(f"\nScenario {scenario['id']}: {scenario['intent'][:50]}...")
            result = evaluate_scenario(scenario, model_key)
            if result:
                all_results.append(result)
                print(f"  ✓ M1={result['m1_fact_recall']} | M2={result['m2_tone_accuracy']} | M3={result['m3_conciseness']} | Avg={result['overall_avg']}")
            time.sleep(0.5)  # gentle rate limit buffer

    # ── Write CSV ─────────────────────────────────────────────────────────────
    csv_path = os.path.join(OUTPUT_DIR, "evaluation_results.csv")
    csv_fields = [
        "scenario_id", "intent", "tone", "model",
        "m1_fact_recall", "m1_facts_found", "m1_total_facts",
        "m2_tone_accuracy",
        "m3_conciseness", "m3_word_count",
        "overall_avg",
        "generated_subject"
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_results)

    # ── Write full JSON ───────────────────────────────────────────────────────
    json_path = os.path.join(OUTPUT_DIR, "evaluation_results.json")
    # Make results JSON serialisable
    json_results = []
    for r in all_results:
        jr = {k: v for k, v in r.items()}
        json_results.append(jr)
    
    with open(json_path, "w") as f:
        json.dump(json_results, f, indent=2)

    # ── Summary stats ─────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("  SUMMARY")
    print("="*60)
    
    summary = {}
    for model_key in MODELS:
        model_results = [r for r in all_results if r["model"] == model_key]
        if not model_results:
            continue
        summary[model_key] = {
            "avg_fact_recall":   round(sum(r["m1_fact_recall"] for r in model_results) / len(model_results), 2),
            "avg_tone_accuracy": round(sum(r["m2_tone_accuracy"] for r in model_results) / len(model_results), 2),
            "avg_conciseness":   round(sum(r["m3_conciseness"] for r in model_results) / len(model_results) , 2),
            "overall_avg":       round(sum(r["overall_avg"] for r in model_results) / len(model_results), 2),
        }
        print(f"\n{model_key.upper()} ({MODELS[model_key]})")
        for k, v in summary[model_key].items():
            print(f"  {k}: {v}/10")

    summary_path = os.path.join(OUTPUT_DIR, "summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n✓ CSV  → {csv_path}")
    print(f"✓ JSON → {json_path}")
    print(f"✓ Summary → {summary_path}")
    
    return all_results, summary


if __name__ == "__main__":
    run_evaluation()
