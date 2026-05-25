"""
classifier.py
LLM-powered EU AI Act risk tier classifier.
Uses GPT-4o-mini with structured prompting to classify AI systems and explain reasoning.
"""
import json
from openai import OpenAI
from .eu_act_knowledge import (
    RISK_TIERS, PROHIBITED_PRACTICES, HIGH_RISK_CATEGORIES,
    OBLIGATIONS, NEXT_STEPS, PUBLIC_SECTOR_NOTES
)


def _build_classification_prompt(system_name: str, description: str, use_case: str,
                                  users: str, decisions: str, sector: str) -> str:
    prohibited = "\n".join(f"- {p}" for p in PROHIBITED_PRACTICES)
    high_risk_summary = ""
    for category, examples in HIGH_RISK_CATEGORIES.items():
        high_risk_summary += f"\n{category}:\n"
        high_risk_summary += "\n".join(f"  - {e}" for e in examples)

    return f"""You are an expert in EU AI Act compliance (Regulation 2024/1689).
Classify the following AI system into one of four risk tiers based on the Act.

RISK TIERS:
- UNACCEPTABLE: Prohibited under Article 5. Cannot be deployed.
- HIGH: Permitted but requires conformity assessment, documentation, human oversight (Annex III).
- LIMITED: Permitted with transparency obligations (must disclose AI to users).
- MINIMAL: No mandatory requirements.

PROHIBITED PRACTICES (Article 5) — classify as UNACCEPTABLE if any apply:
{prohibited}

HIGH-RISK CATEGORIES (Annex III) — classify as HIGH if any apply:
{high_risk_summary}

AI SYSTEM TO CLASSIFY:
Name: {system_name}
Description: {description}
Use case / context: {use_case}
Who uses it / who is affected: {users}
Decisions it makes or influences: {decisions}
Sector: {sector}

IMPORTANT NOTES:
- Educational AI that evaluates, monitors, or scores students = HIGH RISK (Annex III Point 3)
- AI systems affecting children require extra scrutiny
- Public sector AI has stricter accountability requirements
- When in doubt between HIGH and LIMITED, lean toward HIGH for public sector

Respond ONLY with valid JSON in this exact format:
{{
  "tier": "UNACCEPTABLE" | "HIGH" | "LIMITED" | "MINIMAL",
  "confidence": "HIGH" | "MEDIUM" | "LOW",
  "primary_reason": "One sentence explaining the main reason for this classification",
  "article_reference": "The specific Article or Annex that applies (e.g. 'Annex III, Point 3')",
  "key_factors": ["factor 1", "factor 2", "factor 3"],
  "gdpr_flags": ["any GDPR concerns if personal data is involved"],
  "children_flag": true | false
}}"""


def classify_ai_system(
    system_name: str,
    description: str,
    use_case: str,
    users: str,
    decisions: str,
    sector: str,
    api_key: str,
) -> dict:
    """
    Classify an AI system under the EU AI Act.
    Returns a structured result with tier, reasoning, obligations, and next steps.
    """
    client = OpenAI(api_key=api_key)

    prompt = _build_classification_prompt(
        system_name, description, use_case, users, decisions, sector
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an EU AI Act compliance expert. "
                        "Always respond with valid JSON only. No markdown, no explanation outside JSON."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=800,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content
        llm_result = json.loads(raw)
        tier = llm_result.get("tier", "MINIMAL")

        # Enrich with structured knowledge base data
        return {
            "tier": tier,
            "tier_info": RISK_TIERS[tier],
            "confidence": llm_result.get("confidence", "MEDIUM"),
            "primary_reason": llm_result.get("primary_reason", ""),
            "article_reference": llm_result.get("article_reference", ""),
            "key_factors": llm_result.get("key_factors", []),
            "gdpr_flags": llm_result.get("gdpr_flags", []),
            "children_flag": llm_result.get("children_flag", False),
            "obligations": OBLIGATIONS[tier],
            "next_steps": NEXT_STEPS[tier],
            "public_sector_note": PUBLIC_SECTOR_NOTES.get("education", "") if sector.lower() in ["education", "preschool", "school"] else "",
        }

    except json.JSONDecodeError:
        return {"error": "Failed to parse LLM response. Please try again."}
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            return {"error": "Invalid API key. Please check your OpenAI API key in the sidebar."}
        elif "rate_limit" in error_msg.lower():
            return {"error": "Rate limit reached. Please wait a moment and try again."}
        else:
            return {"error": f"Classification failed: {error_msg}"}
