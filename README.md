# EU AI Act Risk Classifier

> Describe any AI system. Get an instant risk tier classification under EU Regulation 2024/1689 — with legal basis, compliance obligations, and actionable next steps.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?logo=streamlit)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green?logo=openai)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## What it does

The EU AI Act (Regulation 2024/1689) classifies AI systems into four risk tiers based on their potential impact on fundamental rights and safety. This tool makes that classification accessible for developers, compliance teams, and public sector organizations deploying AI.

You describe your AI system. The classifier determines:

| Output | Description |
|---|---|
| **Risk Tier** | Unacceptable / High / Limited / Minimal |
| **Legal basis** | Specific Article or Annex that applies |
| **Key factors** | Why the system received that classification |
| **Obligations** | What you are legally required to do |
| **Next steps** | Concrete compliance actions |
| **GDPR flags** | Relevant data protection concerns |
| **Children flag** | Heightened protection alert if minors are affected |

---

## Risk Tiers

| Tier | Meaning |
|---|---|
| 🚫 **Unacceptable** | Prohibited under Article 5. Cannot be deployed in the EU. |
| 🔴 **High Risk** | Permitted but requires conformity assessment, documentation, human oversight (Annex III). |
| 🟡 **Limited Risk** | Permitted with transparency obligations — users must know they interact with AI. |
| 🟢 **Minimal Risk** | No mandatory requirements. Voluntary codes of conduct recommended. |

---

## Live Demo

🔗 https://eu-ai-act-classifier.streamlit.app/ ← **[Try it on Streamlit Cloud]** 

---

## Tech Stack

- **UI:** Streamlit
- **Classification:** OpenAI GPT-4o-mini with JSON mode 
- **Knowledge base:** Structured Python module encoding EU AI Act risk tiers, Annex III categories, Article 5 prohibitions, and per-tier obligations

---

## Project Structure

```
EU-AI-Act-Classifier/
├── app.py                        # Streamlit UI — form, results, obligations display
├── modules/
│   ├── eu_act_knowledge.py       # Structured EU AI Act knowledge base
│   └── classifier.py             # LLM classification logic + knowledge enrichment
├── requirements.txt
├── .env.example
└── README.md
```

---

## How It Works

### Classification pipeline

1. User fills in: system name, description, use case, who is affected, decisions made, sector
2. A structured prompt is built from the input + EU AI Act knowledge (prohibited practices, Annex III categories)
3. GPT-4o-mini classifies the system with `response_format: json_object` for reliable structured output
4. The result is enriched with pre-defined obligations and next steps from `eu_act_knowledge.py`
5. Results are displayed with tier badge, legal reference, obligations checklist, and GDPR flags


### Why hybrid LLM + knowledge base?

The obligations, next steps, and prohibited practices lists are deterministic, they come from the actual text of the regulation. Only the *classification reasoning* (mapping a description to a tier) benefits from LLM reasoning. This prevents the LLM from hallucinating compliance requirements.

---

## Local Setup

```bash
git clone https://github.com/Elfer09/EU-AI-Act-Classifier.git
cd EU-AI-Act-Classifier
pip install -r requirements.txt
```

Add your OpenAI API key in the sidebar when running the app — no `.env` file needed for local use.

```bash
streamlit run app.py
```

---

## Use Cases

- **Public sector organizations** evaluating AI tools before procurement
- **Developers** checking compliance before deployment
- **Compliance teams** building internal AI governance frameworks
- **Education** — understanding how the Act applies to EdTech and school AI systems

---

## Disclaimer

This tool is for educational and informational purposes only. It does not constitute legal advice. Always consult qualified legal counsel for binding compliance decisions.

---

## Roadmap

- [ ] Export classification report as PDF
- [ ] Batch classification via CSV upload
- [ ] GDPR DPIA checklist generator for High-risk systems
- [ ] Sector-specific deep-dive (education, healthcare, HR)
