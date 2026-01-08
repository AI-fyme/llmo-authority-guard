import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import datetime
import json
import re

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="LLMO Authority Guard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STEALTH MODE (Hide Streamlit Branding) ---
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- BRANDING: MODERN SAAS AESTHETIC ---
# Extracted from your reference image (Light, Airy, Purple Gradients)
PRIMARY_COLOR = "#6d28d9"   # Deep Violet (Reference style)
ACCENT_COLOR = "#8b5cf6"    # Lighter Violet for gradients
TEXT_COLOR = "#1e293b"      # Slate 800 (Soft Black)
BG_COLOR = "#f8faff"        # Very light Cloud Blue/Gray
SIDEBAR_BG = "#ffffff"      # Pure White

# Custom CSS for "Clean SaaS" Aesthetic
st.markdown(f"""
    <style>
    /* MAIN BACKGROUND */
    .stApp {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
        font-family: 'Inter', sans-serif;
    }}
    
    .main {{
        background-color: {BG_COLOR};
    }}

    /* HEADINGS */
    h1, h2, h3 {{
        color: #0f172a !important; /* Dark Slate for headers */
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }}
    
    h1 {{
        background: -webkit-linear-gradient(0deg, {PRIMARY_COLOR}, {ACCENT_COLOR});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 10px;
        font-size: 2.5rem !important;
    }}
    
    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {{
        background-color: {SIDEBAR_BG};
        border-right: 1px solid #e2e8f0; /* Light border */
        box-shadow: 4px 0 24px rgba(0,0,0,0.02); /* Very soft shadow */
    }}
    
    /* INPUT FIELDS (Modern clean look) */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
        color: {TEXT_COLOR};
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 10px;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {PRIMARY_COLOR};
        box-shadow: 0 0 0 2px rgba(109, 40, 217, 0.1);
    }}
    
    /* BUTTONS (Gradient & Shadow) */
    .stButton > button {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {ACCENT_COLOR} 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(109, 40, 217, 0.3);
        width: 100%;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 10px 15px -3px rgba(109, 40, 217, 0.4);
        color: white;
    }}

    /* INFO BOXES (Soft Cards) */
    .stAlert {{
        background-color: #ffffff;
        color: {TEXT_COLOR};
        border: 1px solid #e2e8f0;
        border-left: 4px solid {PRIMARY_COLOR};
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-radius: 8px;
    }}
    
    /* CODE BLOCKS */
    .stCodeBlock {{
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}
    
    /* DIVIDERS */
    hr {{
        border: 0;
        border-top: 1px solid #e2e8f0;
        margin: 2rem 0;
    }}
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. HELPER FUNCTIONS
# -----------------------------------------------------------------------------

def validate_url(url):
    """Ensure URL has http/https schema."""
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url

def get_domain(url):
    parsed = urlparse(url)
    return parsed.netloc

# -----------------------------------------------------------------------------
# 2b. LOGIN GATE (UPDATED FOR SAAS AESTHETIC)
# -----------------------------------------------------------------------------

def check_login():
    """Creates a professional Login Form requiring Email."""
    
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        # --- LOGIN SCREEN UI (Clean White Card) ---
        st.markdown("""
            <style>
                .login-box {
                    max-width: 420px; 
                    margin: 0 auto; 
                    padding: 3rem;
                    border: 1px solid #f1f5f9;
                    border-radius: 16px; 
                    background-color: #ffffff; 
                    text-align: center;
                    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("## 🔒 LLMO Authority Guard")
            st.caption("Enter your credentials to access the toolsuite.")
            
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            
            email = st.text_input("Email Address", placeholder="name@company.com")
            password = st.text_input("Access Key", type="password")
            
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            
            if st.button("Login to Dashboard"):
                # CREDENTIALS CHECK
                if email and password == "AI-FY-VIP": 
                    st.session_state["logged_in"] = True
                    st.rerun()
                elif not email:
                    st.error("⚠️ Please enter your email address.")
                else:
                    st.error("❌ Invalid Access Key.")
        
        return False 
    
    return True

# --- EXECUTE LOGIN CHECK ---
if not check_login():
    st.stop()
    
# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🛡️ Authority Guard")
    st.caption("Powered by AI-fy.me")
    st.markdown("---")
    
    selected_module = st.radio(
        "TOOLS MENU",
        (
            "Module A: Robots.txt Architect",
            "Module B: Sitemap Generator",
            "Module C: Schema Builder",
            "Module D: SEO & Meta Engineer"
        )
    )
    
    st.markdown("---")
    st.info(
        "**Why LLM Optimization?**\n\n"
        "Traditional SEO targets Google. "
        "LLMO targets AI models like GPT-4, Gemini, and Claude."
    )

# -----------------------------------------------------------------------------
# 4. MODULE A: ROBOTS.TXT ARCHITECT
# -----------------------------------------------------------------------------
if selected_module == "Module A: Robots.txt Architect":
    st.title("🤖 Robots.txt Architect")
    st.write("Control exactly how AI Bots access and read your site data.")
    
    st.info(
        "**Why this matters:** The `robots.txt` file is the gatekeeper. "
        "By explicitly allowing specific AI bots (like GPTBot), you grant them permission "
        "to read your content, which is the first step to being cited in AI answers."
    )
    
    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Permission Controls")
        st.write("Select the bots you want to explicitly allow:")
        allow_gpt = st.checkbox("Allow GPTBot (OpenAI/ChatGPT)", value=True)
        allow_cc = st.checkbox("Allow CCBot (Common Crawl - Training Data)", value=True)
        allow_perplexity = st.checkbox("Allow PerplexityBot (Answer Engine)", value=True)
        allow_google_ext = st.checkbox("Allow Google-Extended (Bard/Gemini)", value=True)
        
        st.caption("Note: We include 'User-agent: *' by default for general access.")

    with col2:
        st.subheader("2. Generated Code")
        
        # --- THIS WAS THE BROKEN LINE ---
        robots_content = "# Generated by LLMO Authority Guard\n\n"
        
        # General Rule
        robots_content += "User-agent: *\nAllow: /\n\n"
        
        # Specific AI Rules
        if allow_gpt:
            robots_content += "User-agent: GPTBot\nAllow: /\n\n"
        if allow_cc:
            robots_content += "User-agent: CCBot\nAllow: /\n\n"
        if allow_perplexity:
            robots_content += "User-agent: PerplexityBot\nAllow: /\n\n"
        if allow_google_ext:
            robots_content += "User-agent: Google-Extended\nAllow: /\n\n"
            
        st.code(robots_content, language="text")

    with st.expander("🛠️ How to Check & Install"):
        st.markdown("""
        1.  **Copy** the code above.
        2.  **Paste** it into a text file named `robots.txt`.
        3.  **Upload** this file to the "root" folder of your website hosting.
        4.  **Verify** by visiting: `yourdomain.com/robots.txt`.
        """)
