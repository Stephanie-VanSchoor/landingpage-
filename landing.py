import streamlit as st

st.set_page_config(
    page_title="IT Pro - Assistant IT",
    page_icon="🔧",
    layout="wide"
)

st.markdown("""
<!DOCTYPE html>
<html>
<head>
<style>
body {
    font-family: Arial, sans-serif;
    text-align: center;
    background: #0a0a0f;
    color: white;
}

h1 {
    font-size: 48px;
    color: #00d4ff;
}

.btn {
    background: #00d4ff;
    color: #0a0a0f !important;
    padding: 15px 40px;
    border-radius: 8px;
    text-decoration: none;
    font-size:18px;
    font-weight:bold;
    display:inline-block;
    margin:10px;
}

.btn:hover{
    background:#00b8e6;
}

.btn-gold{
    background:#FFD700;
    color:#000 !important;
    padding:15px 40px;
    border-radius:8px;
    text-decoration:none;
    display:inline-block;
    margin:10px;
    font-weight:bold;
}

.btn-dark{
    background:#333;
    color:white !important;
    padding:15px 40px;
    border-radius:8px;
    text-decoration:none;
    display:inline-block;
    margin:10px;
}

.features{
    display:flex;
    justify-content:center;
    gap:30px;
    margin:40px 0;
    flex-wrap:wrap;
}

.feature{
    background:#1a1a2e;
    padding:20px;
    border-radius:12px;
    width:200px;
}

.feature h3{
    color:#00d4ff;
}

.footer{
    margin-top:50px;
    color:#666;
    font-size:14px;
}

.search{
    width:60%;
    max-width:500px;
    padding:15px;
    border-radius:8px;
    border:2px solid #1a1a2e;
    background:#1a1a2e;
    color:white;
    font-size:16px;
}
</style>

<div style="text-align:center">

<h1>🔧 IT Pro - Assistant IT</h1>

<p style="font-size:20px;color:#aaa;">
Diagnostics informatiques & abonnements Pro/Business
</p>

<input class="search" placeholder="Décrivez votre problème...">

<br><br>

<div class="features">

<div class="feature">
<h3>⚡ Rapide</h3>
<p>Résultats en 0,5 seconde</p>
</div>

<div class="feature">
<h3>🔒 Sécurisé</h3>
<p>Mots de passe hachés</p>
</div>

<div class="feature">
<h3>📊 1000+ diagnostics</h3>
<p>Base complète</p>
</div>

</div>

<div style="margin-top:40px">

<a class="btn"
href="https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/"
target="_self">
🚀 Accéder à l'application
</a>

<a class="btn-gold"
href="https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/Offres"
target="_self">
💳 Voir les offres / Payer
</a>

<a class="btn-dark"
href="https://github.com/vanschoor-stephanie/moteur-de-recherche-IT"
target="_blank">
🐙 Voir sur GitHub
</a>

</div>

<div class="footer">

<p>IT Pro - Par Stéphanie Vanschoor</p>

<p>Version 2.0 - 2026</p>

</div>

</div>

</html>
""", unsafe_allow_html=True)
