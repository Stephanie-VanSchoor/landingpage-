import streamlit as st

st.set_page_config(
    page_title="IT Pro",
    page_icon="🔧",
    layout="wide"
)

# CSS
st.markdown("""
<style>

.stApp{
    background: linear-gradient(180deg,#0a0a0f,#111827);
    color:white;
}

h1{
    text-align:center;
    color:#00d4ff;
    font-size:64px;
    margin-bottom:0;
}

.subtitle{
    text-align:center;
    color:#bdbdbd;
    font-size:22px;
    margin-bottom:40px;
}

div[data-testid="stTextInput"] input{
    background:#1a1a2e;
    color:white;
    border-radius:12px;
    border:2px solid #1a1a2e;
    padding:15px;
}

div[data-testid="stTextInput"] input:focus{
    border:2px solid #00d4ff;
}

.feature{
    background:#1a1a2e;
    padding:25px;
    border-radius:15px;
    text-align:center;
    border:1px solid #2b2b45;
    height:180px;
}

.feature h3{
    color:#00d4ff;
}

.footer{
    text-align:center;
    color:#888;
    margin-top:60px;
}

.stButton>button{
    width:100%;
    border-radius:12px;
    height:50px;
    font-size:18px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>🔧 IT Pro</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Assistant IT • Diagnostics • Solutions • Base de connaissances</div>",
    unsafe_allow_html=True,
)

# Barre de recherche
question = st.text_input(
    "",
    placeholder="Décrivez votre problème informatique..."
)

if st.button("🔍 Rechercher"):
    if question:
        st.switch_page("pages/Moteur.py")  # si ton moteur est une page Streamlit
    else:
        st.warning("Veuillez décrire votre problème.")

st.write("")
st.write("")

# Features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature">
        <h3>⚡ Rapide</h3>
        <p>Diagnostic en moins d'une seconde.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature">
        <h3>🔒 Sécurisé</h3>
        <p>Données protégées et navigation sécurisée.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature">
        <h3>📚 +1000 diagnostics</h3>
        <p>Base de connaissances IT complète.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# Boutons
c1, c2, c3 = st.columns(3)

with c1:
    st.link_button(
        "🚀 Accéder à l'application",
        "https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/"
    )

with c2:
    st.link_button(
        "💳 Voir les offres",
        "https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/Offres"
    )

with c3:
    st.link_button(
        "🐙 GitHub",
        "https://github.com/vanschoor-stephanie/moteur-de-recherche-IT"
    )

st.write("")
st.write("---")

st.markdown("""
<div class="footer">
<h3>IT Pro</h3>

Développé par <b>Stéphanie Vanschoor</b>

Version 2.0 • 2026
</div>
""", unsafe_allow_html=True)
