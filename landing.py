import streamlit as st

st.set_page_config(
    page_title="IT Pro",
    page_icon="🔧",
    layout="wide"
)

st.markdown("""
<style>

#MainMenu, footer, header {
    visibility: hidden;
}

.stApp {
    background:#0a0a0f;
    color:white;
}

.hero {
    text-align:center;
    padding:80px 20px 50px;
}

.hero h1 {
    font-size:70px;
    color:#00d4ff;
    margin-bottom:15px;
}

.hero p {
    font-size:25px;
    color:#aaa;
}

.card {
    background:#1a1a2e;
    padding:30px;
    border-radius:15px;
    text-align:center;
    border:1px solid #2a2a4a;
}

.card h3 {
    color:#00d4ff;
    font-size:25px;
}

.card p {
    color:#bbb;
    font-size:16px;
}

.button {
    display:inline-block;
    padding:18px 45px;
    margin:10px;
    border-radius:10px;
    text-decoration:none;
    font-size:18px;
    font-weight:bold;
}

.blue {
    background:#00d4ff;
    color:#000;
}

.gold {
    background:#FFD700;
    color:#000;
}

.dark {
    background:#333;
    color:white;
}

.footer {
    text-align:center;
    margin-top:70px;
    color:#666;
}

</style>
""", unsafe_allow_html=True)


# HERO

st.markdown("""
<div class="hero">

<h1>🔧 IT Pro</h1>

<p>
Assistant IT intelligent<br>
Diagnostics informatiques & solutions professionnelles
</p>

</div>
""", unsafe_allow_html=True)


# FEATURES

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
    <h3>⚡ Rapide</h3>
    <p>
    Trouvez rapidement des solutions
    à vos problèmes informatiques.
    </p>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown("""
    <div class="card">
    <h3>🔒 Sécurisé</h3>
    <p>
    Une plateforme pensée pour
    protéger vos données.
    </p>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown("""
    <div class="card">
    <h3>📚 Expertise IT</h3>
    <p>
    Une base complète de diagnostics
    et solutions techniques.
    </p>
    </div>
    """, unsafe_allow_html=True)
# TARIFS

st.write("")
st.write("")

st.markdown("""
<div style="text-align:center;">

<h2 style="color:#00d4ff;font-size:40px;">
💳 Nos offres
</h2>

<p style="color:#aaa;font-size:18px;">
Choisissez la formule adaptée à vos besoins
</p>

</div>
""", unsafe_allow_html=True)


prix1, prix2, prix3 = st.columns(3)


with prix1:
    st.markdown("""
    <div class="card">

    <h3>🆓 Gratuit</h3>

    <h2 style="color:white;">
    0 €
    </h2>

    <p>
    ✔ Accès découverte<br>
    ✔ Diagnostics de base<br>
    ✔ Recherche limitée
    </p>

    </div>
    """, unsafe_allow_html=True)


with prix2:
    st.markdown("""
    <div class="card" style="border:2px solid #00d4ff;">

    <h3>⭐ Pro</h3>

    <h2 style="color:#00d4ff;">
    9,99 €/mois
    </h2>

    <p>
    ✔ Diagnostics avancés<br>
    ✔ Historique des recherches<br>
    ✔ Support prioritaire
    </p>

    </div>
    """, unsafe_allow_html=True)


with prix3:
    st.markdown("""
    <div class="card">

    <h3>🏢 Business</h3>

    <h2 style="color:#FFD700;">
    29,99 €/mois
    </h2>

    <p>
    ✔ Multi-utilisateurs<br>
    ✔ Solutions entreprise<br>
    ✔ Support renforcé
    </p>

    </div>
    """, unsafe_allow_html=True)


# BOUTONS

st.write("")
st.write("")

st.markdown("""
<div style="text-align:center;">

<a class="button blue"
href="https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/">
🚀 Accéder à l'application
</a>


<a class="button gold"
href="https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/Offres">
💳 Voir les offres Premium
</a>




</div>
""", unsafe_allow_html=True)



# FOOTER

st.markdown("""
<div class="footer">

<b>IT Pro</b><br>
Développé par Stéphanie Vanschoor

<br><br>

Version 2.0 • 2026

</div>
""", unsafe_allow_html=True)
