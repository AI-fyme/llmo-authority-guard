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
    initial_sidebar_state="expanded" # Forces sidebar open
)

# --- BRANDING: MODERN SAAS AESTHETIC ---
PRIMARY_COLOR = "#6d28d9"   # Deep Violet
ACCENT_COLOR = "#8b5cf6"    # Lighter Violet
TEXT_COLOR = "#0f172a"      # Dark Slate
BG_COLOR = "#f8faff"        # Very light Cloud Blue/Gray
SIDEBAR_BG = "#ffffff"      # Pure White

# --- MASTER CSS BLOCK ---
st.markdown(f"""
    <style>
    /* 1. SIDEBAR & HEADER FIXES */
    /* Make header transparent but VISIBLE so the arrow/hamburger are clickable */
    header {{
        visibility: visible !important;
        background: transparent !important;
    }}
    
    /* Hide specific Streamlit items we don't want */
    #MainMenu {{visibility: hidden;}} 
    footer {{visibility: hidden;}}    
    .stDeployButton {{display:none;}} 

    /* 2. MAIN APP STYLING */
    .stApp {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
        font-family: 'Inter', sans-serif;
    }}
    
    .main {{
        background-color: {BG_COLOR};
    }}

    /* 3. TYPOGRAPHY */
    h1, h2, h3 {{
        color: #0f172a !important;
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
    
    /* 4. SIDEBAR STYLING */
    [data-testid="stSidebar"] {{
        background-color: {SIDEBAR_BG};
        border-right: 1px solid #e2e8f0;
        box-shadow: 4px 0 24px rgba(0,0,0,0.02);
    }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
        color: {TEXT_COLOR} !important;
    }}
    
    /* 5. INPUT FIELDS */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
        color: {TEXT_COLOR};
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 10px;
    }}
    
    /* 6. BUTTONS */
    .stButton > button {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {ACCENT_COLOR} 100%);
        color: white !important;
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
    }}

    /* 7. INFO BOXES & CARDS */
    .stAlert {{
        background-color: #ffffff;
        color: {TEXT_COLOR};
        border: 1px solid #e2e8f0;
        border-left: 4px solid {PRIMARY_COLOR};
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-radius: 8px;
    }}
    
    .stCodeBlock {{
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}

    /* 8. VISIBILITY FIXES FOR TEXT */
    .stCheckbox label p, .stRadio label p {{
        color: {TEXT_COLOR} !important;
        font-weight: 500;
    }}
    p {{
        color: {TEXT_COLOR};
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
# 2b. LOGIN GATE
# -----------------------------------------------------------------------------

def check_login():
    """Creates a professional Login Form requiring Email."""
    
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        # --- LOGIN UI ---
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
        
        robots_content = "# Generated by LLMO Authority Guard\n\n"
        robots_content += "User-agent: *\nAllow: /\n\n"
        
        if allow_gpt:
            robots_content += "User-agent: GPTBot\nAllow: /\n\n"
        if allow_cc:
            robots_content += "User-agent: CCBot\nAllow: /\n\n"
        if allow_perplexity:
            robots_content += "User-agent: PerplexityBot\nAllow: /\n\n"
        if allow_google_ext:
            robots_content += "User-agent: Google-Extended\nAllow: /\n\n"
            
        st.code(robots_content, language="text")

    with st.expander("🛠️ How to Check & Install", expanded=False):
        st.markdown("""
        **Installation Steps:**
        1.  **Copy** the code generated in the black box above.
        2.  **Paste** it into a new text file named `robots.txt` on your computer.
        3.  **Upload** this file to the "root" folder of your website hosting (public_html).
        4.  **Verify** the installation by visiting: `yourdomain.com/robots.txt`.
        """)

# -----------------------------------------------------------------------------
# 5. MODULE B: SITEMAP GENERATOR
# -----------------------------------------------------------------------------
elif selected_module == "Module B: Sitemap Generator":
    st.title("🗺️ Sitemap Generator")
    st.write("Map your most important pages so AI models can find them.")
    
    st.info(
        "**Why this matters:** A clean XML sitemap helps LLMs discover deep pages "
        "that might otherwise be missed during a crawl."
    )

    st.subheader("1. Scan Website")
    target_url = st.text_input("Enter your website URL:", placeholder="https://mysite.com")
    
    generate_btn = st.button("Attempt Auto-Scan")
    
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
        
        with st.expander("🚀 Where to Submit", expanded=False):
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
    st.write("Create the code that establishes your digital identity.")
    
    st.info(
        "**Why this matters:** Schema (JSON-LD) is the language machines speak. "
        "It tells LLMs explicitly who you are and connects your website to your LinkedIn."
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
    st.title("⚙️ SEO & Meta Engineer")
    st.write("Generate the perfect HTML headers for your pages.")
    
    st.info(
        "**Why this matters:** Title tags and Meta descriptions are the first thing an LLM reads. "
        "They determine how the AI summarizes your page."
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
