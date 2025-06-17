import streamlit as st
import streamlit.components.v1 as components
from upload_tool import process_upload, requirements
from PIL import Image
import io
from logger import logger
import os

# Page config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "static", "logo_tool.png")
favicon_path = os.path.join(BASE_DIR, "static", "favicon.png")
st.set_page_config(
    page_title="ATK-WPBR Resize-Tool",
    page_icon=favicon_path,
    layout="centered"
)

logger.info("Applicatie gestart")

# Google Analytics G-tag injectie
components.html(
    '''
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BLVYVZBXHK"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-BLVYVZBXHK');
    </script>
    ''',
    height=0,
) 

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .image-preview {
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 5px;
    }
    /* Hand-cursor voor selectbox */
    .stSelectbox [data-baseweb="select"] {cursor: pointer;}
    .stSelectbox [data-baseweb="select"]:hover {cursor: pointer;}
    </style>
    """, unsafe_allow_html=True)

# Branding/logo bovenaan
st.image(logo_path, width=320)

# Header
st.title("ATK-WPBR Resize-Tool")
st.markdown("""
    **Automatisch juiste foto's voor WPBR-aanvragen**
    
    Met deze tool past u eenvoudig uw afbeeldingen aan naar de officiële WPBR aanvraag-eisen. Zo voorkomt u afwijzingen door verkeerde formaten.
    
    *Let op: deze tool is alleen bedoeld voor het aanpassen van afbeeldingen voor de ATK-aanvragen voor de WPBR.*
    """,)
    
# File uploader
image_type = st.radio(
    "Selecteer type afbeelding",
    ["pasfoto", "handtekening", "bedrijfslogo"],
    horizontal=False
)
logger.debug(f"Geselecteerd afbeeldingstype: {image_type}")

uploaded_file = st.file_uploader(
    "Upload uw afbeelding",
    type=["jpg", "jpeg", "png"],
    help="Ondersteunde formaten: JPG, JPEG, PNG"
)

if uploaded_file is not None:
    logger.info(f"Bestand geüpload: {uploaded_file.name}")
    
    # Process the image
    result = process_upload(uploaded_file, image_type)
    
    if result['success']:
        # Display original and resized dimensions
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Originele afmetingen", f"{result['orig_size'][0]} x {result['orig_size'][1]} pixels")
        with col2:
            st.metric("Nieuwe afmetingen", f"{result['resized_size'][0]} x {result['resized_size'][1]} pixels")
        
        # Display requirements
        st.info(f"Minimale afmetingen: {result['min_size'][0]} x {result['min_size'][1]} pixels\n"
                f"Maximale afmetingen: {result['max_size'][0]} x {result['max_size'][1]} pixels")
        
        # Display preview
        st.subheader("Voorbeeld")
        img_bytes = io.BytesIO()
        result['image'].save(img_bytes, format='PNG')
        st.image(img_bytes, width=result['resized_size'][0])
        
        # Download button
        st.download_button(
            label="Download geresizede afbeelding",
            data=img_bytes.getvalue(),
            file_name=f"resized_{uploaded_file.name}",
            mime="image/png"
        )
        logger.info(f"Afbeelding succesvol verwerkt en weergegeven: {uploaded_file.name}")
    else:
        st.error(f"Fout bij verwerken: {result['error']}")
        logger.error(f"Fout bij verwerken {uploaded_file.name}: {result['error']}")

# Simple Login/Registration System
st.subheader("Login/Registratie")
with st.form("login_form"):
    username = st.text_input("Gebruikersnaam")
    password = st.text_input("Wachtwoord", type="password")
    login_submitted = st.form_submit_button("Inloggen")
    if login_submitted:
        # Simulate login logic
        if username == "admin" and password == "password":
            st.success("Ingelogd als admin")
            st.session_state['logged_in'] = True
        else:
            st.error("Ongeldige gebruikersnaam of wachtwoord")

with st.form("register_form"):
    new_username = st.text_input("Nieuwe Gebruikersnaam")
    new_password = st.text_input("Nieuw Wachtwoord", type="password")
    register_submitted = st.form_submit_button("Registreren")
    if register_submitted:
        # Simulate registration logic
        st.success(f"Geregistreerd als {new_username}")

# Check if user is logged in
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning("Log in om de tool te gebruiken.")
    st.stop()

# Footer
st.markdown("---")
st.markdown("""
<div style='font-size: 0.95em; color: #888; text-align: center;'>
Deze afbeeldingen zijn automatisch geresized met de <b>ATK-WPBR Resize-Tool</b>: een gestandaardiseerde tool voor het correct en foutloos aanleveren van aanvragen m.b.t. de WPBR.<br>
<b>© 2025 ATK-WPBR Resize-Tool</b><br>
<a href='https://www.atk-wpbr.nl' target='_blank'>www.atk-wpbr.nl</a> | support@atk-wpbr.nl
 | <a href='#' onclick="window.parent.document.querySelector('aside [data-baseweb=select]').value='Privacyverklaring';window.location.reload();return false;">Privacyverklaring</a>
<div style='font-size: 0.85em; color: #888;'>
    Deze tool is ontwikkeld door <b><a href='https://snuushco.github.io/' style='color: #888; text-decoration: underline;'>Snuushco's Software Solutions</a></b> in opdracht van <b><a href='https://www.praesidion.nl' target='_blank' style='color: #888; text-decoration: underline;'>Praesidion Security</a></b>.<br>
</div>
<div style='font-size: 0.85em; color: #888; margin-top: 0.5em;'>
    Deze site gebruikt cookies voor statistieken en gebruiksanalyse. Door verder te gaan accepteert u dit.
</div>
</div>
""", unsafe_allow_html=True)

