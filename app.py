import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SMS Spam Detector // AI Cyber Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# 2. CUSTOM FUTURISTIC & GLASSMORPHISM CSS
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

/* Theme Color Tokens */
:root {
    --bg-dark: #070b14;
    --card-bg: rgba(13, 20, 36, 0.75);
    --card-border: rgba(255, 255, 255, 0.08);
    --cyan-glow: #00f2fe;
    --cyan-accent: #00e5ff;
    --violet-glow: #7928ca;
    --violet-accent: #8b5cf6;
    --spam-red: #ff3366;
    --ham-green: #00f59b;
}

/* Cosmic Animated Background */
.stApp {
    background-color: #070b14 !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.16) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(0, 242, 254, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.12) 0px, transparent 50%),
        radial-gradient(at 0% 100%, rgba(121, 40, 202, 0.16) 0px, transparent 50%);
    background-attachment: fixed;
    font-family: 'Space Grotesk', sans-serif !important;
    color: #e2e8f0 !important;
}

/* Hide Default Streamlit Header & Footer */
header[data-testid="stHeader"] {
    background: transparent !important;
}
#MainMenu, footer {
    visibility: hidden;
    height: 0;
}

/* Centered Container Constraints */
.block-container {
    max-width: 860px !important;
    padding-top: 2rem !important;
    padding-bottom: 3.5rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}

/* Glassmorphism Outer Panel */
.glass-panel {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 24px;
    padding: 2.2rem 2.2rem 1.8rem 2.2rem;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6), 0 0 40px rgba(0, 242, 254, 0.05);
    position: relative;
    overflow: hidden;
    margin-bottom: 1.6rem;
}

.glass-panel::before {
    content: '';
    position: absolute;
    top: 0;
    left: -50%;
    width: 200%;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan-glow), var(--violet-glow), transparent);
    animation: borderScan 8s linear infinite;
}

@keyframes borderScan {
    0% { transform: translateX(-30%); }
    100% { transform: translateX(30%); }
}

/* Hero Section */
.hero-wrapper {
    text-align: center;
    margin-bottom: 1.8rem;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0, 242, 254, 0.08);
    border: 1px solid rgba(0, 242, 254, 0.3);
    border-radius: 50px;
    padding: 6px 16px;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: var(--cyan-accent);
    margin-bottom: 1rem;
    box-shadow: 0 0 15px rgba(0, 242, 254, 0.15);
}

.pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--cyan-glow);
    box-shadow: 0 0 8px var(--cyan-glow);
    animation: pulseGlow 2s infinite;
}

@keyframes pulseGlow {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 242, 254, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(0, 242, 254, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 242, 254, 0); }
}

.hero-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 2.6rem !important;
    font-weight: 900 !important;
    letter-spacing: 1.5px !important;
    line-height: 1.15 !important;
    margin: 0 0 0.8rem 0 !important;
    color: #ffffff !important;
}

.gradient-title {
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 35%, #8b5cf6 75%, #d946ef 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(0, 242, 254, 0.3);
}

.hero-description {
    font-size: 1rem;
    color: #94a3b8;
    line-height: 1.6;
    max-width: 640px;
    margin: 0 auto 1.2rem auto;
}

.hero-description strong {
    color: #f1f5f9;
}

.tag-list {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 0.5rem;
}

.tag-badge {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 0.78rem;
    color: #cbd5e1;
    font-weight: 500;
}

/* Form Headings */
.section-label {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.2px;
    color: #64748b;
    margin-bottom: 0.6rem;
    text-transform: uppercase;
}

/* Polished Text Area */
div[data-baseweb="textarea"] {
    background: rgba(10, 16, 30, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 16px !important;
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.45) !important;
    transition: all 0.3s ease !important;
}

div[data-baseweb="textarea"]:focus-within {
    border-color: var(--cyan-glow) !important;
    box-shadow: 0 0 20px rgba(0, 242, 254, 0.25), inset 0 2px 6px rgba(0, 0, 0, 0.45) !important;
}

textarea {
    color: #f8fafc !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.02rem !important;
    line-height: 1.6 !important;
}

textarea::placeholder {
    color: #64748b !important;
    font-size: 0.92rem !important;
}

/* Base Buttons */
.stButton > button {
    border-radius: 12px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Primary "Analyze" Button: Glowing Cyan-Violet Gradient */
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 35%, #7928ca 80%, #d946ef 100%) !important;
    background-size: 200% 200% !important;
    color: #ffffff !important;
    border: none !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    box-shadow: 0 4px 25px rgba(0, 242, 254, 0.35), 0 0 15px rgba(121, 40, 202, 0.25) !important;
    width: 100% !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    transform: translateY(-2px) scale(1.008) !important;
    box-shadow: 0 8px 35px rgba(0, 242, 254, 0.55), 0 0 25px rgba(121, 40, 202, 0.45) !important;
    filter: brightness(1.12) !important;
}

.stButton > button[kind="primary"]:active,
.stButton > button[data-testid="stBaseButton-primary"]:active {
    transform: translateY(1px) scale(0.99) !important;
}

/* Secondary Quick-Test Buttons */
.stButton > button[kind="secondary"],
.stButton > button[data-testid="stBaseButton-secondary"] {
    background: rgba(15, 23, 42, 0.65) !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 0.45rem 0.8rem !important;
}

.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="stBaseButton-secondary"]:hover {
    background: rgba(30, 41, 59, 0.8) !important;
    color: #ffffff !important;
    border-color: rgba(0, 242, 254, 0.4) !important;
    box-shadow: 0 0 15px rgba(0, 242, 254, 0.15) !important;
}

/* Dynamic Result Cards */
.result-card {
    border-radius: 20px;
    padding: 1.8rem 2.2rem;
    margin-top: 1.8rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    animation: fadeInSlide 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeInSlide {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Spam Result: Neon Crimson Glow */
.result-spam {
    background: linear-gradient(135deg, rgba(255, 51, 102, 0.12) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(255, 51, 102, 0.5);
    box-shadow: 0 10px 40px rgba(255, 51, 102, 0.25), 0 0 30px rgba(255, 51, 102, 0.15), inset 0 0 15px rgba(255, 51, 102, 0.06);
}

/* Ham Result: Neon Emerald Glow */
.result-ham {
    background: linear-gradient(135deg, rgba(0, 245, 155, 0.12) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(0, 245, 155, 0.5);
    box-shadow: 0 10px 40px rgba(0, 245, 155, 0.22), 0 0 30px rgba(0, 245, 155, 0.15), inset 0 0 15px rgba(0, 245, 155, 0.06);
}

.result-header {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    margin-bottom: 1rem;
}

.result-icon-box {
    width: 54px;
    height: 54px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.icon-spam {
    background: rgba(255, 51, 102, 0.15);
    border: 1px solid rgba(255, 51, 102, 0.4);
    box-shadow: 0 0 20px rgba(255, 51, 102, 0.3);
}

.icon-ham {
    background: rgba(0, 245, 155, 0.15);
    border: 1px solid rgba(0, 245, 155, 0.4);
    box-shadow: 0 0 20px rgba(0, 245, 155, 0.3);
}

.badge-tag-spam {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.2px;
    color: var(--spam-red);
    text-transform: uppercase;
}

.badge-tag-ham {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.2px;
    color: var(--ham-green);
    text-transform: uppercase;
}

.result-title-spam {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #ff3366;
    margin: 0;
    text-shadow: 0 0 20px rgba(255, 51, 102, 0.4);
}

.result-title-ham {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #00f59b;
    margin: 0;
    text-shadow: 0 0 20px rgba(0, 245, 155, 0.4);
}

.result-divider {
    height: 1px;
    width: 100%;
    margin: 0.9rem 0 1rem 0;
}

.divider-spam {
    background: linear-gradient(90deg, rgba(255, 51, 102, 0.4), transparent);
}

.divider-ham {
    background: linear-gradient(90deg, rgba(0, 245, 155, 0.4), transparent);
}

.result-explanation {
    font-size: 0.96rem;
    line-height: 1.6;
    color: #cbd5e1;
    margin-bottom: 0.9rem;
}

.result-meta-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 500;
}

.meta-spam {
    background: rgba(255, 51, 102, 0.1);
    border: 1px solid rgba(255, 51, 102, 0.25);
    color: #fca5a5;
}

.meta-ham {
    background: rgba(0, 245, 155, 0.1);
    border: 1px solid rgba(0, 245, 155, 0.25);
    color: #86efac;
}

/* Confidence Meter Bar */
.confidence-box {
    margin-top: 1.1rem;
    background: rgba(0, 0, 0, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
}

.confidence-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.45rem;
}

.confidence-label {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1px;
    color: #94a3b8;
}

.confidence-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.88rem;
    font-weight: 800;
}

.meter-track {
    width: 100%;
    height: 6px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    overflow: hidden;
}

.meter-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Footer */
.footer-container {
    margin-top: 2.8rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    text-align: center;
}

.footer-info {
    font-size: 0.84rem;
    color: #64748b;
    margin-bottom: 0.8rem;
    line-height: 1.5;
}

.footer-info strong {
    color: #94a3b8;
}

.footer-links-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.2rem;
    flex-wrap: wrap;
}

.gh-badge-link {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 6px 14px;
    color: #cbd5e1 !important;
    text-decoration: none !important;
    font-size: 0.82rem;
    font-weight: 600;
    transition: all 0.25s ease;
}

.gh-badge-link:hover {
    background: rgba(255, 255, 255, 0.09);
    border-color: var(--cyan-glow);
    color: #ffffff !important;
    box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
    transform: translateY(-1px);
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. NLTK PREPARATION & PREPROCESSING (ORIGINAL LOGIC INTACT)
# -----------------------------------------------------------------------------
# Download required NLTK corpora safely (prevents Streamlit Cloud / offline crashes)
for corpus in ["punkt", "punkt_tab", "stopwords"]:
    try:
        nltk.download(corpus, quiet=True)
    except Exception:
        pass

ps = PorterStemmer()

def transform_text(Text):
    Text = Text.lower()
    # tokenization
    Text = nltk.word_tokenize(Text)
    # Remove Special Characters (englih ya Alphanumeric)
    y = []
    for i in Text:
        if i.isalnum():
            y.append(i)

    Text = y[:]
    # upar jo kiya hai uska mtlb ye hai ki list ko aap kabhi bhi aise assign nhi kr skte kyuki list is mutable so we need to clone and assign like this
    y.clear()
    # remove stop words (jinka sentence formation me mtlb hota hai lkn genrealy meaning nhi hota is, are, etc)

    for i in Text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    Text = y[:]
    # further process of stemming
    y.clear()

    for i in Text:
        y.append(ps.stem(i))

    return " ".join(y)

# -----------------------------------------------------------------------------
# 4. LOAD TRAINED MODEL & TF-IDF VECTORIZER
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_ml_assets():
    try:
        with open('vectorizer.pkl', 'rb') as f_vec:
            tfidf_loaded = pickle.load(f_vec)
        with open('model.pkl', 'rb') as f_mod:
            model_loaded = pickle.load(f_mod)
        return tfidf_loaded, model_loaded
    except FileNotFoundError:
        return None, None

tfidf, model = load_ml_assets()

# -----------------------------------------------------------------------------
# 5. HERO SECTION
# -----------------------------------------------------------------------------
hero_html = """
<div class="glass-panel">
    <div class="hero-wrapper">
        <div class="hero-badge">
            <span class="pulse-dot"></span>
            <span>CYBER DEFENSE INTELLIGENCE</span>
            <span>&bull; v2.0</span>
        </div>
        <h1 class="hero-title">
            SENTINEL <span class="gradient-title">SPAM SHIELD</span>
        </h1>
        <p class="hero-description">
            Next-generation SMS threat detection engine. Inspects message semantics via 
            <strong>NLTK tokenization</strong>, <strong>TF-IDF vectorization</strong>, and 
            a trained <strong>Machine Learning classifier</strong>.
        </p>
        <div class="tag-list">
            <span class="tag-badge">⚡ TF-IDF Vectorizer</span>
            <span class="tag-badge">🧠 Scikit-Learn Classifier</span>
            <span class="tag-badge">🛡️ Real-Time Inference</span>
            <span class="tag-badge">🔬 Natural Language Processing</span>
        </div>
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# Guard against missing pickle files
if tfidf is None or model is None:
    st.error("⚠️ **Model Artifacts Not Found:** Please ensure `vectorizer.pkl` and `model.pkl` are present in the app's root directory.")
    st.stop()

# -----------------------------------------------------------------------------
# 6. INPUT SECTION & INTERACTIVE PRESETS
# -----------------------------------------------------------------------------
if "sms_input" not in st.session_state:
    st.session_state.sms_input = ""

st.markdown('<div class="section-label">QUICK TEST SAMPLES</div>', unsafe_allow_html=True)
col_preset1, col_preset2, col_clear = st.columns([1, 1, 0.6])

with col_preset1:
    if st.button("🚨 Load Spam Example", type="secondary", use_container_width=True):
        st.session_state.sms_input = "URGENT! You have won a 1-week holiday to the Caribbean or £5,000 cash! Claim your prize now by texting WIN to 87121. T&Cs apply."

with col_preset2:
    if st.button("💬 Load Safe Example", type="secondary", use_container_width=True):
        st.session_state.sms_input = "Hey Chitransh, let's schedule our project review call for 4 PM today. Let me know if that time works for you!"

with col_clear:
    if st.button("🔄 Clear", type="secondary", use_container_width=True):
        st.session_state.sms_input = ""

st.markdown('<div class="section-label" style="margin-top: 1rem;">INPUT MESSAGE</div>', unsafe_allow_html=True)
input_sms = st.text_area(
    label="Message Content",
    value=st.session_state.sms_input,
    placeholder="Paste or type an SMS / Email message here to inspect its threat profile (e.g. promotional offers, urgent bank alerts, or personal chats)...",
    height=140,
    label_visibility="collapsed"
)

# Analyze Action Button
analyze_clicked = st.button("⚡ ANALYZE MESSAGE", type="primary", use_container_width=True)

# -----------------------------------------------------------------------------
# 7. PREDICTION PIPELINE & DYNAMIC RESULT CARD
# -----------------------------------------------------------------------------
if analyze_clicked:
    if not input_sms.strip():
        st.warning("⚠️ Please enter or paste a message above before running analysis.")
    else:
        with st.spinner("Analyzing semantic structure & vectorizing tokens..."):
            # 1. Preprocess
            transformed_sms = transform_text(input_sms)
            # 2. Vectorize
            vector_input = tfidf.transform([transformed_sms])
            # 3. Predict
            result = model.predict(vector_input)[0]

            # Optional confidence calculation if classifier provides probabilities
            confidence_val = None
            if hasattr(model, "predict_proba"):
                try:
                    probs = model.predict_proba(vector_input)[0]
                    confidence_val = round(float(probs[result]) * 100, 1)
                except Exception:
                    confidence_val = None

        # Render Dynamic Result Card
        if result == 1:
            # SPAM RESULT CARD
            conf_bar = ""
            if confidence_val is not None:
                conf_bar = f"""
                <div class="confidence-box">
                    <div class="confidence-header">
                        <span class="confidence-label">MODEL CERTAINTY</span>
                        <span class="confidence-value" style="color: #ff3366;">{confidence_val}%</span>
                    </div>
                    <div class="meter-track">
                        <div class="meter-fill" style="width: {confidence_val}%; background: #ff3366; box-shadow: 0 0 10px #ff3366;"></div>
                    </div>
                </div>
                """

            spam_card_html = f"""
            <div class="result-card result-spam">
                <div class="result-header">
                    <div class="result-icon-box icon-spam">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#ff3366" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                            <line x1="12" y1="9" x2="12" y2="13"></line>
                            <line x1="12" y1="17" x2="12.01" y2="17"></line>
                        </svg>
                    </div>
                    <div>
                        <div class="badge-tag-spam">THREAT DETECTED</div>
                        <h2 class="result-title-spam">SPAM / MALICIOUS</h2>
                    </div>
                </div>
                <div class="result-divider divider-spam"></div>
                <p class="result-explanation">
                    <strong>High Threat Risk:</strong> The linguistic features, promotional vocabulary, and token density match patterns strongly correlated with unsolicited marketing, phishing deception, or fraudulent scams.
                </p>
                <div class="result-meta-pill meta-spam">
                    <span>⚠️</span>
                    <span><strong>Advisory:</strong> Do not click untrusted links, reply with credentials, or dial callback numbers.</span>
                </div>
                {conf_bar}
            </div>
            """
            st.markdown(spam_card_html, unsafe_allow_html=True)

        else:
            # NOT SPAM (HAM) RESULT CARD
            conf_bar = ""
            if confidence_val is not None:
                conf_bar = f"""
                <div class="confidence-box">
                    <div class="confidence-header">
                        <span class="confidence-label">MODEL CERTAINTY</span>
                        <span class="confidence-value" style="color: #00f59b;">{confidence_val}%</span>
                    </div>
                    <div class="meter-track">
                        <div class="meter-fill" style="width: {confidence_val}%; background: #00f59b; box-shadow: 0 0 10px #00f59b;"></div>
                    </div>
                </div>
                """

            ham_card_html = f"""
            <div class="result-card result-ham">
                <div class="result-header">
                    <div class="result-icon-box icon-ham">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#00f59b" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                            <polyline points="9 12 11 14 15 10"></polyline>
                        </svg>
                    </div>
                    <div>
                        <div class="badge-tag-ham">VERIFIED SAFE</div>
                        <h2 class="result-title-ham">NOT SPAM (HAM)</h2>
                    </div>
                </div>
                <div class="result-divider divider-ham"></div>
                <p class="result-explanation">
                    <strong>Clean Communication:</strong> The token sequence and stems reflect authentic, organic conversational communication with negligible risk markers or deceptive triggers.
                </p>
                <div class="result-meta-pill meta-ham">
                    <span>🛡️</span>
                    <span><strong>Status:</strong> Clear of known spam triggers. Safe for standard interaction.</span>
                </div>
                {conf_bar}
            </div>
            """
            st.markdown(ham_card_html, unsafe_allow_html=True)

        # Inspection Expander
        with st.expander("🔍 View NLP Preprocessing & Pipeline Breakdown"):
            st.write("**Transformed Stems:**")
            st.code(transformed_sms if transformed_sms else "(Empty stem sequence)", language="text")
            st.caption("Lowercased, tokenized via NLTK, alphanumeric filtered, stopwords & punctuation removed, Porter stemmed.")

# -----------------------------------------------------------------------------
# 8. FOOTER SECTION
# -----------------------------------------------------------------------------
footer_html = """
<div class="footer-container">
    <p class="footer-info">
        Engineered with <strong>TF-IDF Vectorization</strong> + <strong>Multinomial Naive Bayes</strong>, 
        trained on the <strong>SMS Spam Collection dataset</strong>.
    </p>
    <div class="footer-links-row">
        <a href="https://github.com/Chitranshsri/SMS-Spam-Detection" target="_blank" class="gh-badge-link">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
            </svg>
            <span>GitHub: Chitranshsri / SMS-Spam-Detection</span>
        </a>
    </div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
