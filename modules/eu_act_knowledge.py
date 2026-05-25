"""
eu_act_knowledge.py
Structured knowledge base for the EU AI Act (Regulation 2024/1689).
Covers risk tiers, prohibited practices, high-risk categories, and obligations.
"""

RISK_TIERS = {
    "UNACCEPTABLE": {
        "label": "🚫 Unacceptable Risk",
        "color": "#e74c3c",
        "summary": "Prohibited under Article 5. This AI system cannot be deployed in the EU.",
        "description": (
            "AI systems in this category pose unacceptable risks to fundamental rights, "
            "safety, or democratic values. They are strictly prohibited under Article 5 "
            "of the EU AI Act."
        ),
    },
    "HIGH": {
        "label": "🔴 High Risk",
        "color": "#e67e22",
        "summary": "Permitted but subject to strict obligations before deployment (Annex III).",
        "description": (
            "High-risk AI systems may be deployed but require conformity assessments, "
            "technical documentation, human oversight mechanisms, and registration in "
            "the EU database before market placement."
        ),
    },
    "LIMITED": {
        "label": "🟡 Limited Risk",
        "color": "#f1c40f",
        "summary": "Permitted with transparency obligations — users must know they are interacting with AI.",
        "description": (
            "Limited-risk systems face specific transparency requirements. Users must be "
            "informed they are interacting with an AI system, particularly for chatbots, "
            "deepfakes, and AI-generated content."
        ),
    },
    "MINIMAL": {
        "label": "🟢 Minimal Risk",
        "color": "#2ecc71",
        "summary": "No specific obligations. Voluntary codes of conduct recommended.",
        "description": (
            "The vast majority of AI systems fall into this category. No mandatory "
            "requirements apply, though providers are encouraged to follow voluntary "
            "codes of conduct."
        ),
    },
}

PROHIBITED_PRACTICES = [
    "Social scoring or ranking of individuals by public authorities based on behavior",
    "Real-time remote biometric identification in public spaces for law enforcement",
    "Subliminal manipulation that distorts behavior causing harm",
    "Exploitation of vulnerabilities based on age, disability, or social situation",
    "Biometric categorization inferring race, political opinions, religion, or sexual orientation",
    "Predictive policing based solely on profiling without objective evidence",
    "Emotion recognition in workplace or educational settings",
    "Untargeted scraping of facial images from internet or CCTV for facial recognition databases",
]

HIGH_RISK_CATEGORIES = {
    "Biometric identification": [
        "Remote biometric identification (non-real-time)",
        "Biometric categorization of natural persons",
        "Emotion recognition systems",
    ],
    "Critical infrastructure": [
        "Safety components in road traffic, water, gas, heating, electricity",
        "Digital infrastructure management",
    ],
    "Education and training": [
        "Determining access or admission to educational institutions",
        "Evaluating learning outcomes and student performance",
        "Monitoring and detecting prohibited behavior during exams",
        "Assessing appropriate level of education for individuals",
    ],
    "Employment and workers": [
        "Recruitment and selection of natural persons",
        "Making decisions on promotion, termination, task allocation",
        "Monitoring and evaluating worker performance",
    ],
    "Essential services": [
        "Creditworthiness assessment",
        "Risk assessment for life/health insurance",
        "Emergency services dispatch prioritization",
        "Eligibility for public assistance benefits",
    ],
    "Law enforcement": [
        "Assessing risk of criminal offenses",
        "Polygraph-style lie detection",
        "Evaluating reliability of evidence in investigations",
        "Profiling in criminal investigations",
    ],
    "Migration and border": [
        "Risk assessment of irregular migration",
        "Examination of visa/asylum applications",
        "Border security monitoring",
    ],
    "Justice and democracy": [
        "Assisting judicial authorities in fact-finding or law interpretation",
        "Influencing election outcomes or voter behavior",
    ],
}

OBLIGATIONS = {
    "UNACCEPTABLE": [
        "❌ System must not be developed, placed on market, or put into service",
        "❌ Existing deployments must be discontinued",
        "📋 Legal counsel required before any further action",
    ],
    "HIGH": [
        "📄 Technical documentation (Article 11) — detailed system documentation required",
        "📋 Conformity assessment — internal or third-party review before deployment",
        "🗄️ EU database registration — mandatory registration before market placement",
        "👁️ Human oversight measures — humans must be able to monitor, intervene, and override",
        "📊 Risk management system — continuous identification and mitigation of risks",
        "🔍 Data governance — training data must meet quality criteria, bias monitored",
        "📝 Logging & audit trail — automatic recording of system operation logs",
        "🔔 Post-market monitoring — ongoing monitoring after deployment",
        "⚠️ Serious incident reporting — notify authorities of serious incidents",
        "♿ Accessibility — must meet accessibility requirements",
    ],
    "LIMITED": [
        "💬 Transparency disclosure — users must be informed they interact with AI",
        "🎭 Deepfake labeling — AI-generated content must be labeled as such",
        "🤖 Chatbot disclosure — chatbots must identify themselves as AI on request",
    ],
    "MINIMAL": [
        "✅ No mandatory requirements under the EU AI Act",
        "📘 Voluntary codes of conduct are recommended",
        "🔒 General GDPR obligations still apply if personal data is processed",
    ],
}

PUBLIC_SECTOR_NOTES = {
    "education": (
        "AI systems used in educational contexts that evaluate, monitor, or make decisions "
        "about students are classified as HIGH RISK under Annex III, Point 3. This includes "
        "attendance monitoring, behavioral assessment, learning analytics, and adaptive "
        "learning platforms that influence educational outcomes."
    ),
    "children": (
        "When AI systems process data about or make decisions affecting children (under 18), "
        "heightened protection applies. GDPR Article 8 requires parental consent. The EU AI "
        "Act's prohibited practices on vulnerability exploitation apply with extra force."
    ),
    "gdpr_intersection": (
        "High-risk AI systems in the public sector must comply with both the EU AI Act AND GDPR. "
        "Key intersections: Article 22 GDPR (automated decision-making), data minimization, "
        "purpose limitation, and DPIAs which may overlap with AI Act conformity assessments."
    ),
}

NEXT_STEPS = {
    "UNACCEPTABLE": [
        "Immediately halt development and deployment",
        "Consult legal counsel familiar with EU AI Act",
        "Explore alternative approaches that do not fall under prohibited practices",
        "Document the decision and reasoning for compliance records",
    ],
    "HIGH": [
        "Appoint an AI compliance officer or designate responsibility",
        "Begin technical documentation (Article 11 requirements)",
        "Commission or conduct a conformity assessment",
        "Register the system in the EU AI Act database",
        "Design and implement human oversight mechanisms",
        "Set up post-market monitoring procedures",
        "Conduct a DPIA if personal data is involved (GDPR Article 35)",
        "Establish an incident reporting pipeline",
    ],
    "LIMITED": [
        "Add clear disclosure to the user interface ('You are talking to an AI')",
        "Ensure chatbot identifies itself when users ask if it is human",
        "Label AI-generated content appropriately",
        "Review GDPR obligations if personal data is processed",
    ],
    "MINIMAL": [
        "No immediate action required under the EU AI Act",
        "Consider adopting voluntary codes of conduct",
        "Ensure GDPR compliance if personal data is processed",
        "Document AI usage for internal governance purposes",
    ],
}
