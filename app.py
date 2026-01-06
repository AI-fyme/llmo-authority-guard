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

# --- BRANDING: DARK ARCHITECT THEME ---
# Updated to match a modern AI/Dark Web Aesthetic
PRIMARY_COLOR = "#5710ff"   # Electric Purple
ACCENT_COLOR = "#cb6ce6"    # Soft Purple
TEXT_COLOR = "#e0e0e0"      # Light Grey (for dark mode)
BG_COLOR = "#0e1117"        # Dark Streamlit BG
PANEL_BG = "#161b22"        # Slightly lighter for cards/sidebar

# Custom CSS for "Dark Blueprint" Aesthetic
st.markdown(f"""
    <style>
    /* FORCE DARK MODE BACKGROUNDS */
    .stApp {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
    }}
    
    .main {{
        background-color: {BG_COLOR};
        font-family: 'Courier New', Courier, monospace; 
    }}

    /* HEADINGS */
    h1, h2, h3 {{
        color: white !important; /* White text for contrast */
        font-family: 'Arial', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    h1 {{
        border-bottom: 3px solid {PRIMARY_COLOR}; /* Purple Underline */
        padding-bottom: 10px;
    }}
    
    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {{
        background-color: {PANEL_BG};
        border-right: 1px solid #30363d;
    }}
    
    /* INPUT FIELDS (Dark Mode Fix) */
    .stTextInput > div > div > input {{
        color: white;
        background-color: #0d1117;
        border: 1px solid #30363d;
    }}
    
    /* BUTTONS */
    .stButton > button {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        transition: all 0.3s;
        width: 100%; /* Full width buttons look better */
    }}
    .stButton > button:hover {{
        background-color: {ACCENT_COLOR};
        box-shadow: 0 0 10px {PRIMARY_COLOR}; /* Glowing effect */
    }}

    /* INFO BOXES (Alerts) */
    .stAlert {{
        background-color: {PANEL_BG};
        color: {TEXT_COLOR};
        border-left: 4px solid {ACCENT_COLOR};
    }}
    
    /* CODE BLOCKS */
    .stCodeBlock {{
        border: 1px solid #30363d;
        border-radius: 5px;
        background-color: #000000;
    }}
    
    /* DIVIDERS */
    hr {{
        border: 0;
        border-top: 1px dashed #30363d;
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
# 2b. LOGIN GATE (UPDATED FOR DARK MODE)
# -----------------------------------------------------------------------------

def check_login():
    """Creates a professional Login Form requiring Email."""
    
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        # --- LOGIN SCREEN UI (Dark Version) ---
        st.markdown("""
            <style>
                .login-box {
                    max-width: 400px; 
                    margin: 0 auto; 
                    padding: 40px;
                    border: 1px solid #30363d; 
                    border-radius: 10px; 
                    background-color: #161b22; 
                    text-align: center;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
                }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("## 🔒 LLMO Authority Guard")
            st.info("Please sign in to access the Architect Tools.")
            
            email = st.text_input("Email Address", placeholder="name@company.com")
            password = st.text_input("Access Key", type="password")
            
            if st.button("Login"):
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
    st.markdown(f"# 🛡️ LLMO Authority")
    st.markdown(f"### *Powered by AI-fy.me*")
    st.markdown("---")
    
    selected_module = st.radio(
        "Select Optimization Module:",
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
        "LLMO targets AI models like GPT-4, Gemini, and Claude, "
        "ensuring they can read, understand, and cite your business data."
    )

# -----------------------------------------------------------------------------
# 4. MODULE A: ROBOTS.TXT ARCHITECT
# -----------------------------------------------------------------------------
if selected_module == "Module A: Robots.txt Architect":
    st.title("🤖 Robots.txt Architect")
    st.markdown("### Control How AI Bots Access Your Site")
    
    st.info(
        "**Educational Note:** The `robots.txt` file is the gatekeeper of your website. "
        "By explicitly allowing AI bots, you grant them permission to read your content, "
        "which is the first step to being cited in AI answers."
    )

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Select Bots to Allow")
        allow_gpt = st.checkbox("Allow GPTBot (OpenAI/ChatGPT)", value=True)
        allow_cc = st.checkbox("Allow CCBot (Common Crawl - Used by many LLMs)", value=True)
        allow_perplexity = st.checkbox("Allow PerplexityBot", value=True)
        allow_google_ext = st.checkbox("Allow Google-Extended (Bard/Gemini)", value=True)
        
        st.caption("Note: 'User-agent: *' is included by default for general access.")

    with col2:
        st.subheader("2. Preview Code")
        
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

# -----------------------------------------------------------------------------
# 5. MODULE B: SITEMAP GENERATOR
# -----------------------------------------------------------------------------
elif selected_module == "Module B: Sitemap Generator":
    st.title("🗺️ Sitemap Generator & Guide")
    st.markdown("### Map Your Content for AI Discovery")
    
    st.info(
        "**Educational Note:** A Sitemap is an XML map of your website. "
        "It helps LLMs and Search Engines find pages they might otherwise miss. "
        "A clean sitemap = better indexing."
    )

    st.subheader("1. Scan Website")
    target_url = st.text_input("Enter your website URL (e.g., https://mysite.com):", placeholder="https://")
    
    generate_btn = st.button("Attempt Auto-Generation")
    
    if 'sitemap_urls' not in st.session_state:
        st.session_state['sitemap_urls'] = []
    if 'use_manual' not in st.session_state:
        st.session_state['use_manual'] = False

    if generate_btn and target_url:
        target_url = validate_url(target_url)
        st.write(f"Scanning {target_url}...")
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(target_url, headers=headers, timeout=5)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            base_domain = get_domain(target_url)
            
            found_links = set()
            found_links.add(target_url.rstrip('/'))
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(target_url, href)
                
                if get_domain(full_url) == base_domain:
                    clean_url = full_url.split('#')[0].split('?')[0]
                    if clean_url.startswith('http'): 
                        found_links.add(clean_url)
            
            if len(found_links) < 2:
                st.warning("Could not find enough links automatically. Switching to Manual Builder.")
                st.session_state['use_manual'] = True
            else:
                st.session_state['sitemap_urls'] = list(found_links)[:50] 
                st.session_state['use_manual'] = False
                st.success(f"Success! Found {len(st.session_state['sitemap_urls'])} internal URLs.")
                
        except Exception as e:
            st.error(f"Auto-scan failed (Site might block bots or have security headers). Error: {e}")
            st.session_state['use_manual'] = True

    if st.session_state['use_manual']:
        st.markdown("---")
        st.subheader("✏️ Manual Sitemap Builder")
        st.caption("Since we couldn't scan the site perfectly, please list your 5 most important pages below.")
        
        with st.form("manual_sitemap_form"):
            url_1 = st.text_input("Homepage URL", value=target_url if target_url else "")
            url_2 = st.text_input("Service/Product Page 1")
            url_3 = st.text_input("Service/Product Page 2")
            url_4 = st.text_input("About Us Page")
            url_5 = st.text_input("Contact/Blog Page")
            
            submit_manual = st.form_submit_button("Generate XML from List")
            
            if submit_manual:
                manual_list = [u for u in [url_1, url_2, url_3, url_4, url_5] if u.strip()]
                st.session_state['sitemap_urls'] = [validate_url(u) for u in manual_list]

    if st.session_state['sitemap_urls']:
        st.subheader("2. Generated XML Code")
        
        current_date = datetime.date.today().isoformat()
        xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_output += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        for url in st.session_state['sitemap_urls']:
            xml_output += '  <url>\n'
            xml_output += f'    <loc>{url}</loc>\n'
            xml_output += f'    <lastmod>{current_date}</lastmod>\n'
            xml_output += '    <changefreq>monthly</changefreq>\n'
            xml_output += '    <priority>0.8</priority>\n'
            xml_output += '  </url>\n'
        
        xml_output += '</urlset>'
        
        st.code(xml_output, language='xml')
        
        with st.expander("🚀 Where to Submit"):
            st.markdown("""
            1.  Save the code above as `sitemap.xml`.
            2.  Upload it to your root directory (`yourdomain.com/sitemap.xml`).
            3.  Go to **Google Search Console** > **Sitemaps**.
            4.  Enter the URL of your sitemap and click Submit.
            """)

# -----------------------------------------------------------------------------
# 6. MODULE C: SCHEMA BUILDER
# -----------------------------------------------------------------------------
elif selected_module == "Module C: Schema Builder":
    st.title("🏗️ Schema \"Ground Truth\" Builder")
    st.markdown("### Establish Your Digital Identity")
    
    st.info(
        "**Educational Note:** Schema (JSON-LD) is code that talks directly to machines. "
        "It tells LLMs exactly who you are, what you do, and which social profiles belong to you. "
        "This creates a 'Ground Truth' for your brand entity."
    )

    col_input, col_output = st.columns(2)
    
    with col_input:
        st.subheader("1. Entity Details")
        schema_type = st.selectbox("Entity Type", ["Person", "Organization"])
        name = st.text_input("Name (Person or Company Name)")
        title_role = st.text_input("Job Title / Industry", help="E.g., CEO, Consultant, or 'Marketing Agency'")
        website = st.text_input("Website URL")
        bio = st.text_area("Short Bio", height=100, placeholder="A brief description of who you are...")
        
        st.markdown("**'SameAs' Links (Social Proof)**")
        linkedin = st.text_input("LinkedIn URL")
        twitter = st.text_input("X / Twitter URL")
        other_social = st.text_input("Other URL (YouTube/Facebook)")

    with col_output:
        st.subheader("2. JSON-LD Output")
        
        schema_data = {
            "@context": "https://schema.org",
            "@type": schema_type,
            "name": name if name else "[Name]",
            "url": website if website else "[Website URL]",
            "description": bio if bio else "[Bio]",
            "sameAs": []
        }
        
        if schema_type == "Person":
            schema_data["jobTitle"] = title_role
        else:
            schema_data["industry"] = title_role
            
        if linkedin: schema_data["sameAs"].append(linkedin)
        if twitter: schema_data["sameAs"].append(twitter)
        if other_social: schema_data["sameAs"].append(other_social)
        
        json_string = json.dumps(schema_data, indent=2)
        
        html_wrapper = f"""<script type="application/ld+json">
{json_string}
</script>"""
        
        st.code(html_wrapper, language="html")
        
        st.success("✅ Ready to Paste! Place this code into the <head> or <body> of your homepage.")

# -----------------------------------------------------------------------------
# 7. MODULE D: SEO & META DATA ENGINEER
# -----------------------------------------------------------------------------
elif selected_module == "Module D: SEO & Meta Engineer":
    st.title("⚙️ SEO & Meta Data Engineer")
    st.markdown("### Perfect Your Page Headers")
    
    st.info(
        "**Educational Note:** Meta tags are the first thing an LLM reads to understand a page's context. "
        "A clear Title and Description help the AI summarize your content accurately for users."
    )

    with st.form("meta_form"):
        st.subheader("Basic Metadata")
        page_title = st.text_input("Page Title", max_chars=60, help="Keep under 60 characters for best display.")
        
        desc_col1, desc_col2 = st.columns([3, 1])
        with desc_col1:
            meta_desc = st.text_area("Meta Description", max_chars=300, height=100)
        with desc_col2:
            st.metric("Char Count", len(meta_desc))
            if len(meta_desc) > 160:
                st.warning("⚠️ Over 160 chars.")
            else:
                st.success("Length Good.")

        keywords = st.text_input("Keywords (Comma separated)", placeholder="LLM, AI optimization, consulting")
        author = st.text_input("Author Name")
        
        st.markdown("---")
        st.subheader("Advanced Configuration")
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            canonical = st.checkbox("Generate Canonical Link (Self-referencing)", value=True)
            page_url = st.text_input("Full Page URL (for Canonical)", disabled=not canonical)
            
        with col_adv2:
            st.markdown("**Robots Meta Instructions**")
            index_opt = st.checkbox("index (Allow indexing)", value=True)
            follow_opt = st.checkbox("follow (Follow links)", value=True)
        
        generate_meta = st.form_submit_button("Generate HTML Block")

    if generate_meta:
        st.subheader("Output HTML")
        
        robots_directives = []
        robots_directives.append("index" if index_opt else "noindex")
        robots_directives.append("follow" if follow_opt else "nofollow")
        robots_str = ", ".join(robots_directives)
        
        html_block = f"""<title>{page_title}</title>
<meta name="description" content="{meta_desc}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="{author}">
<meta name="robots" content="{robots_str}">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
"""
        if canonical and page_url:
            html_block += f'<link rel="canonical" href="{page_url}">\n'
            
        st.code(html_block, language="html")
        st.info("Copy this block and paste it between the `<head>` and `</head>` tags of your HTML file.")
