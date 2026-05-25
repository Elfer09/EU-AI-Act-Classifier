"""
EU AI Act Risk Classifier — Streamlit application.
Classifies AI systems into risk tiers under EU Regulation 2024/1689.
"""
import streamlit as st
from modules.classifier import classify_ai_system
from modules.eu_act_knowledge import RISK_TIERS, HIGH_RISK_CATEGORIES

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EU AI Act Risk Classifier",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚖️ EU AI Act Classifier")
    st.caption("Based on EU Regulation 2024/1689")
    st.divider()

    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Your key is used only for this session and never stored.",
    )
    st.caption("🔒 Key is never stored or logged.")
    st.divider()

    st.markdown("### About the EU AI Act")
    st.markdown(
        "The EU AI Act (2024/1689) classifies AI systems into **4 risk tiers** "
        "based on their potential impact on fundamental rights and safety. "
        "It applies to providers and deployers of AI systems in the EU."
    )
    st.divider()

    with st.expander("📋 High-Risk Categories (Annex III)"):
        for category, examples in HIGH_RISK_CATEGORIES.items():
            st.markdown(f"**{category}**")
            for ex in examples:
                st.markdown(f"- {ex}")

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("EU AI Act Risk Classifier")
st.markdown(
    "Describe your AI system and get an instant classification under the EU AI Act — "
    "with applicable obligations, compliance steps, and GDPR flags."
)
st.divider()

# ── Preset Examples ────────────────────────────────────────────────────────────
st.subheader("Try an Example")
examples = {
    "Select an example...": None,
    "📚 Student performance prediction (school)": {
        "name": "LearningPredict",
        "description": "Machine learning model that predicts student risk of failing based on grades, attendance, and behavioral data.",
        "use_case": "Early intervention — teachers and counselors use it to identify students who need extra support.",
        "users": "Teachers, school counselors, school administration. Affects students aged 6-18.",
        "decisions": "Flags students as 'at risk' and recommends intervention. Influences resource allocation.",
        "sector": "Education",
    },
    "🤖 HR recruitment chatbot": {
        "name": "HireBot",
        "description": "Chatbot that screens job applications and conducts initial candidate interviews via text.",
        "use_case": "First-stage recruitment screening for job openings.",
        "users": "Job applicants (general public). HR managers review chatbot-generated scores.",
        "decisions": "Scores candidates and decides who advances to human interview stage.",
        "sector": "Employment",
    },
    "💬 Customer service chatbot (municipality)": {
        "name": "MunicipalAssist",
        "description": "Conversational AI that answers citizen questions about municipal services, opening hours, and procedures.",
        "use_case": "Citizen support and information service for a Swedish municipality.",
        "users": "General public — citizens of all ages contacting the municipality.",
        "decisions": "Provides information only. No binding decisions. Escalates complex cases to humans.",
        "sector": "Public administration",
    },
    "📊 Spam filter for internal email": {
        "name": "MailGuard",
        "description": "ML-based spam and phishing detection for internal organizational email.",
        "use_case": "Automated filtering of incoming email to protect organization from phishing attacks.",
        "users": "Internal employees. Emails flagged as spam are moved to junk folder.",
        "decisions": "Classifies emails as spam/not-spam. No decisions about people.",
        "sector": "IT / Cybersecurity",
    },
}

selected = st.selectbox("Load a preset example:", list(examples.keys()))
preset = examples[selected]

# ── Input Form ─────────────────────────────────────────────────────────────────
st.subheader("Describe Your AI System")

col1, col2 = st.columns(2)

with col1:
    system_name = st.text_input(
        "System Name",
        value=preset["name"] if preset else "",
        placeholder="e.g. StudentPredict, HireBot, ChatAssist",
    )
    description = st.text_area(
        "What does the system do?",
        value=preset["description"] if preset else "",
        placeholder="Describe the AI system's functionality, inputs, and outputs.",
        height=120,
    )
    use_case = st.text_area(
        "Use Case & Context",
        value=preset["use_case"] if preset else "",
        placeholder="Where and how is it used? What problem does it solve?",
        height=100,
    )

with col2:
    sector = st.selectbox(
        "Sector",
        [
            "Education",
            "Employment / HR",
            "Healthcare",
            "Law enforcement",
            "Public administration",
            "Finance / Insurance",
            "Migration / Border",
            "Critical infrastructure",
            "IT / Cybersecurity",
            "Retail / E-commerce",
            "Other",
        ],
        index=0 if not preset else [
            "Education", "Employment / HR", "Healthcare", "Law enforcement",
            "Public administration", "Finance / Insurance", "Migration / Border",
            "Critical infrastructure", "IT / Cybersecurity", "Retail / E-commerce", "Other"
        ].index(preset.get("sector", "Other")) if preset.get("sector") in [
            "Education", "Employment / HR", "Healthcare", "Law enforcement",
            "Public administration", "Finance / Insurance", "Migration / Border",
            "Critical infrastructure", "IT / Cybersecurity", "Retail / E-commerce", "Other"
        ] else 10,
    )
    users = st.text_area(
        "Who uses it / who is affected?",
        value=preset["users"] if preset else "",
        placeholder="Who operates the system? Who are the affected individuals?",
        height=100,
    )
    decisions = st.text_area(
        "What decisions does it make or influence?",
        value=preset["decisions"] if preset else "",
        placeholder="Describe any decisions, scores, rankings, or recommendations the system produces.",
        height=100,
    )

st.divider()

# ── Classify Button ────────────────────────────────────────────────────────────
classify_btn = st.button("🔍 Classify under EU AI Act", type="primary", use_container_width=True)

if classify_btn:
    if not api_key:
        st.warning("Add your OpenAI API key in the sidebar to run the classifier.")
        st.stop()
    if not description or not decisions:
        st.warning("Please fill in at least the system description and decisions fields.")
        st.stop()

    with st.spinner("Analysing under EU AI Act framework..."):
        result = classify_ai_system(
            system_name=system_name or "Unnamed System",
            description=description,
            use_case=use_case,
            users=users,
            decisions=decisions,
            sector=sector,
            api_key=api_key,
        )

    if "error" in result:
        st.error(result["error"])
        st.stop()

    # ── Results ────────────────────────────────────────────────────────────────
    tier = result["tier"]
    tier_info = result["tier_info"]

    st.divider()
    st.subheader("Classification Result")

    # Tier badge
    st.markdown(
        f"<h2 style='color:{tier_info['color']}'>{tier_info['label']}</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(f"**{tier_info['summary']}**")

    conf_color = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}.get(result["confidence"], "🟡")
    st.caption(f"{conf_color} Confidence: {result['confidence']}")

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### Why this classification?")
        st.markdown(f"**{result['primary_reason']}**")
        if result.get("article_reference"):
            st.markdown(f"📖 Legal basis: `{result['article_reference']}`")

        st.markdown("**Key factors:**")
        for factor in result.get("key_factors", []):
            st.markdown(f"- {factor}")

        if result.get("children_flag"):
            st.warning(
                "⚠️ **Children's data detected.** "
                "Heightened protection applies under GDPR Article 8 and the EU AI Act's "
                "vulnerability exploitation prohibition."
            )

        if result.get("gdpr_flags"):
            st.markdown("**GDPR flags:**")
            for flag in result["gdpr_flags"]:
                st.markdown(f"- 🔒 {flag}")

    with col_b:
        st.markdown("### Applicable Obligations")
        for obligation in result.get("obligations", []):
            st.markdown(f"- {obligation}")

    st.divider()

    st.markdown("### Next Steps")
    for i, step in enumerate(result.get("next_steps", []), 1):
        st.markdown(f"**{i}.** {step}")

    if result.get("public_sector_note"):
        st.divider()
        st.info(f"🏫 **Education sector note:** {result['public_sector_note']}")

    # ── Tier explanation card ──────────────────────────────────────────────────
    with st.expander("📖 About this risk tier"):
        st.markdown(tier_info["description"])

# ── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "This tool is for educational and informational purposes only. "
    "It does not constitute legal advice. Always consult qualified legal counsel "
    "for binding compliance decisions. Based on EU Regulation 2024/1689 (EU AI Act)."
)
