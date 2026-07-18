import streamlit as st

st.set_page_config(
    page_title="IT Pro",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

/* Cache le menu Streamlit */
#MainMenu, footer, header {
    visibility: hidden;
}

.stApp{
    background:#0a0a0f;
    color:white;
}

.hero{
    text-align:center;
    padding:60px 20px 40px;
}

.hero h1{
    font-size:70px;
    color:#00d4ff;
    margin-bottom:10px;
}

.hero p{
    font-size:24px;
    color:#bdbdbd;
}

.card{
    background:#151525;
    padding:30px;
    border-radius:15px;
    border:1px solid #2a2a45;
    text-align:center;
    transition:.3s;
}

.card:hover{
    border-color:#00d4ff;
    transform:translateY(-6px);
}

.card h3{
    color:#00d4ff;
}

.center{
    text-align:center;
}

.bigbutton{
    display:inline-block;
    padding:18px 45px;
    margin:10px;
    border-radius:12px;
    text-decoration:none;
    font-size:20px;
    font-weight:bold;
}

.blue{
    background:#00d4ff;
    color:black;
}

.gold{
    background:#FFD700;
    color:black;
}

.dark{
    background:#333;
    color:white;
}

.footer{
    text-align:center;
    color:#777;
    margin-top:60px;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">

<h1>🔧 IT Pro</h1>

<p>
L'assistant intelligent pour le diagnostic informatique
</p>

</div>
""", unsafe_allow_html=True)

question = st.text_input(
    "",
    placeholder="💬 Décrivez votre problème informatique..."
)

col = st.columns([1,2,1])

with col[1]:
    st.button("🔍 Rechercher", use_container_width=True)

st.write("")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
<div class="card">
<h3>⚡ Rapide</h3>
<p>
Diagnostic en quelques secondes.
</p>
</div>
""", unsafe_allow_html=True)

with c2:
    st.markdown("""
<div class="card">
<h3>🔒 Sécurisé</h3>
<p>
Vos données restent protégées.
</p>
</div>
""", unsafe_allow_html=True)

with c3:
    st.markdown("""
<div class="card">
<h3>📚 +1000 solutions</h3>
<p>
Une base de connaissances complète.
</p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

st.markdown("""
<div class="center">

<a class="bigbutton blue"
href="https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/">
🚀 Accéder à l'application
</a>

<a class="bigbutton gold"
href="https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/Offres">
💳 Offres Premium
</a>

<a class="bigbutton dark"
href="https://github.com/vanschoor-stephanie/moteur-de-recherche-IT">
🐙 GitHub
</a>

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("---")

st.markdown("""
<div class="footer">

<b>IT Pro</b><br>

Développé par Stéphanie Vanschoor

<br><br>

Version 2.0 • 2026

</div>
""", unsafe_allow_html=True)
