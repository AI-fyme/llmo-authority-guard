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

# --- BRANDING: GLASS & AIR AESTHETIC ---
# Palette: Deep Violet primary, with airy white/translucent surfaces
PRIMARY_COLOR = "#6d28d9"
ACCENT_COLOR = "#a78bfa"
TEXT_COLOR = "#1e293b"      # Slate 800
BG_GRADIENT_START = "#f8faff" # Cool White
BG_GRADIENT_END = "#eef2ff"   # Very faint violet tint

# Custom CSS for "Glass & Air" Design
st.markdown(f"""
    <style>
    /* 1. RESTORE SIDEBAR ARROW (Crucial Fix) */
    header {{
        visibility: visible !important;
        background: transparent !important;
    }}
    /* Hide only the hamburger menu and footer, leave the sidebar arrow */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}} /* Hides the Deploy button */

    /* 2. MAIN BACKGROUND (Subtle Gradient) */
    .stApp {{
        background: linear-gradient(135deg, {BG_GRADIENT_START} 0%, {BG_GRADIENT_END} 100%);
        font-family: 'Inter', system-ui, sans-serif;
    }}
    
    /* 3. TYPOGRAPHY & HEADERS */
    h1, h2, h3 {{
        color: {TEXT_COLOR} !important;
        font-family: 'Inter', system-ui, sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }}
    
    h1 {{
        background: -webkit-linear-gradient(0deg, #5b21b6, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        padding-bottom: 0.5rem;
    }}
    
    /* 4. GLASS CARDS (Login, Alerts, Expanders) */
    /* This creates the "frosted glass" look */
    .stAlert, .login-box, .streamlit-expanderContent {{
        background: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        border-radius: 12px;
        color: {TEXT_COLOR};
    }}
    
    /* 5. SIDEBAR STYLING */
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255, 0.5);
    }}
    /* Sidebar Text Fix */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
        color: {TEXT_COLOR} !important;
    }}
    
    /* 6. INPUT FIELDS (Clean & Soft) */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
        background-color: rgba(255, 255, 255, 0.8);
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        color: {TEXT_COLOR};
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {PRIMARY_COLOR};
        box-shadow: 0 0 0 3px rgba(109, 40, 217, 0.1);
    }}
    
    /* 7. BUTTONS (Vivid Gradient Pills) */
    .stButton > button {{
        background: linear-gradient(90deg, {PRIMARY_COLOR}, #8b5cf6);
        color: white !important;
        border: none;
        border-radius: 50px; /* Pill shape */
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        box-shadow: 0 4px 12px rgba(109, 40, 217, 0.25);
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(109, 40, 217, 0.35);
    }}

    /* 8. CHECKBOXES (Visibility Fix) */
    .stCheckbox label p {{
        color: {TEXT_COLOR} !important;
    }}
    
    /* 9. CODE BLOCKS */
    .stCodeBlock {{
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. HELPER FUNCTIONS
# -----------------------------------------------------------------------------

def validate_url(url):
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url

def get_domain(url):
    parsed = urlparse(url)
    return parsed.netloc

# -----------------------------------------------------------------------------
# 2b. LOGIN GATE (GLASS EDITION)
# -----------------------------------------------------------------------------

def check_login():
    """Creates a professional Login Form."""
    
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        # --- LOGIN UI ---
        st.markdown("""
            <style>
                .login-box {
                    max-width: 400px; 
                    margin: 0 auto; 
                    padding: 3rem;
                    /* Glass effect moved to main CSS block for consistency */
                    text-align: center;
                }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            # We use a container to apply the glass class
            with st.container():
                st.markdown('<div class="login-box">', unsafe_allow_html=True)
                st.markdown("## 🔒 Authority Guard")
                st.caption("Secure Client Access")
                
                st.markdown("---")
                
                email = st.text_input("Email Address", placeholder="name@company.com")
                password = st.text_input("Access Key", type="password")
                
                st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                
                if st.button("Unlock Dashboard"):
                    if email and password == "AI-FY-VIP": 
                        st.session_state["logged_in"] = True
                        st.rerun()
                    elif not email:
                        st.error("⚠️ Please enter your email.")
                    else:
                        st.error("❌ Invalid Access Key.")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        return False 
    
    return True

# --- EXECUTE LOGIN CHECK ---
if not check_login():
    st.stop()
    
# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🛡️ Authority")
    st.caption("Architecture Suite v1.0")
    st.markdown("---")
    
    selected_module = st.radio(
        "NAVIGATION",
        (
            "Module A: Robots.txt Architect",
            "Module B: Sitemap Generator",
            "Module C: Schema Builder",
            "Module D: SEO & Meta Engineer"
        )
    )
    
    st.markdown("---")
    st.info(
        "**LLM Optimization**\n\n"
        "Ensure GPT-4, Gemini, and Claude can read, understand, and cite your business data."
    )

# -----------------------------------------------------------------------------
# 4. MODULE A: ROBOTS.TXT ARCHITECT
# -----------------------------------------------------------------------------
if selected_module == "Module A: Robots.txt Architect":
    st.title("🤖 Robots.txt Architect")
    st.write("Control exactly how AI Bots access and read your site data.")
    
    st.info(
        "**Why this matters:** The `robots.txt` file is the gatekeeper. "
        "By explicitly allowing specific AI bots, you grant them permission "
        "to read your content—the first step to being cited."
    )
    
    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Permission Controls")
        st.write("Select bots to Allow:")
        allow_gpt = st.checkbox("Allow GPTBot (OpenAI)", value=True)
        allow_cc = st.checkbox("Allow CCBot (Common Crawl)", value=True)
        allow_perplexity = st.checkbox("Allow PerplexityBot", value=True)
        allow_google_ext = st.checkbox("Allow Google-Extended", value=True)
        
        st.caption("Note: 'User-agent: *' included by default.")

    with col2:
        st.subheader("2. Generated Code")
        
        robots_content = "# Generated by LLMO Authority Guard\n\n"
        robots_content += "User-agent: *\nAllow: /\n\n"
        
        if allow_gpt: robots_content += "User-agent: GPTBot\nAllow: /\n\n"
        if allow_cc: robots_content += "User-agent: CCBot\nAllow: /\n\n"
        if allow_perplexity: robots_content += "User-agent: PerplexityBot\nAllow: /\n\n"
        if allow_google_ext: robots_content += "User-agent: Google-Extended\nAllow: /\n\n"
            
        st.code(robots_content, language="text")

    with st.expander("🛠️ How to Check & Install", expanded=False):
        st.markdown("""
        1.  **Copy** the code above.
        2.  **Paste** it into a file named `robots.txt`.
        3.  **Upload** to your website's root folder.
        4.  **Verify** at: `yourdomain.com/robots.txt`.
        """)

# -----------------------------------------------------------------------------
# 5. MODULE B: SITEMAP GENERATOR
# -----------------------------------------------------------------------------
elif selected_module == "Module B: Sitemap Generator":
    st.title("🗺️ Sitemap Generator")
    st.write("Map your most important pages so AI models can find them.")
    
    st.info("**Why this matters:** Helps LLMs discover deep pages missed during standard crawls.")

    st.subheader("1. Scan Website")
    target_url = st.text_input("Enter website URL:", placeholder="https://mysite.com")
    
    generate_btn = st.button("Attempt Auto-Scan")
    
    if 'sitemap_urls' not in st.session_state: st.session_state['sitemap_urls'] = []
    if 'use_manual' not in st.session_state: st.session_state['use_manual'] = False

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
                    if clean_url.startswith('http'): found_links.add(clean_url)
            
            if len(found_links) < 2:
                st.warning("Auto-scan found few links. Switching to Manual.")
                st.session_state['use_manual'] = True
            else:
                st.session_state['sitemap_urls'] = list(found_links)[:50] 
                st.session_state['use_manual'] = False
                st.success(f"Success! Found {len(st.session_state['sitemap_urls'])} URLs.")
                
        except Exception as e:
            st.error(f"Scan failed: {e}")
            st.session_state['use_manual'] = True

    if st.session_state['use_manual']:
        st.markdown("---")
        st.subheader("✏️ Manual Builder")
        with st.form("manual_sitemap_form"):
            url_1 = st.text_input("Homepage URL", value=target_url if target_url else "")
            url_2 = st.text_input("Service Page 1")
            url_3 = st.text_input("Service Page 2")
            url_4 = st.text_input("About Page")
            url_5 = st.text_input("Contact Page")
            if st.form_submit_button("Generate XML"):
                manual_list = [u for u in [url_1, url_2, url_3, url_4, url_5] if u.strip()]
                st.session_state['sitemap_urls'] = [validate_url(u) for u in manual_list]

    if st.session_state['sitemap_urls']:
        st.subheader("2. Generated XML")
        current_date = datetime.date.today().isoformat()
        xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for url in st.session_state['sitemap_urls']:
            xml_output += f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{current_date}</lastmod>\n    <priority>0.8</priority>\n  </url>\n'
        xml_output += '</urlset>'
        
        st.code(xml_output, language='xml')
        
        with st.expander("🚀 Where to Submit"):
            st.write("Save as `sitemap.xml`, upload to root, and submit to Google Search Console.")

# -----------------------------------------------------------------------------
# 6. MODULE C: SCHEMA BUILDER
# -----------------------------------------------------------------------------
elif selected_module == "Module C: Schema Builder":
    st.title("🏗️ Schema Builder")
    st.write("Establish your digital identity (Ground Truth).")
    
    col_input, col_output = st.columns(2)
    with col_input:
        st.subheader("1. Entity Details")
        schema_type = st.selectbox("Type", ["Person", "Organization"])
        name = st.text_input("Name")
        title_role = st.text_input("Job Title / Industry")
        website = st.text_input("Website URL")
        bio = st.text_area("Short Bio")
        
        st.markdown("**Social Proof**")
        linkedin = st.text_input("LinkedIn")
        twitter = st.text_input("Twitter/X")
        other = st.text_input("Other URL")

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
        if schema_type == "Person": schema_data["jobTitle"] = title_role
        else: schema_data["industry"] = title_role
        if linkedin: schema_data["sameAs"].append(linkedin)
        if twitter: schema_data["sameAs"].append(twitter)
        if other: schema_data["sameAs"].append(other)
        
        json_string = json.dumps(schema_data, indent=2)
        st.code(f'<script type="application/ld+json">\n{json_string}\n</script>', language="html")
        st.success("Paste this into the <head> of your homepage.")

# -----------------------------------------------------------------------------
# 7. MODULE D: SEO ENGINEER
# -----------------------------------------------------------------------------
elif selected_module == "Module D: SEO & Meta Engineer":
    st.title("⚙️ SEO & Meta Engineer")
    st.write("Generate perfect HTML headers.")

    with st.form("meta_form"):
        st.subheader("Basic Metadata")
        page_title = st.text_input("Page Title", max_chars=60)
        meta_desc = st.text_area("Meta Description", max_chars=300)
        keywords = st.text_input("Keywords")
        author = st.text_input("Author")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            canonical = st.checkbox("Canonical Link", value=True)
            page_url = st.text_input("Full URL", disabled=not canonical)
        with col2:
            st.markdown("**Robots**")
            index_opt = st.checkbox("Index", value=True)
            follow_opt = st.checkbox("Follow", value=True)
        
        if st.form_submit_button("Generate HTML"):
            st.subheader("Output")
            robots = f"{'index' if index_opt else 'noindex'}, {'follow' if follow_opt else 'nofollow'}"
            html = f"""<title>{page_title}</title>
<meta name="description" content="{meta_desc}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="{author}">
<meta name="robots" content="{robots}">
<meta name="viewport" content="width=device-width, initial-scale=1.0">"""
            if canonical and page_url: html += f'\n<link rel="canonical" href="{page_url}">'
            st.code(html, language="html")
