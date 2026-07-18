import streamlit as st

st.set_page_config(
    page_title="IT Pro - Assistant IT",
    page_icon="🔧",
    layout="wide"
)

html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>IT Pro - Assistant IT</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background: #0a0a0f;
            color: white;
        }

        h1 {
            font-size: 48px;
            color: #00d4ff;
        }

        .btn {
            background: #00d4ff;
            color: #0a0a0f;
            padding: 15px 40px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 10px;
        }

        .btn:hover {
            background: #00b8e6;
        }

        .btn-gold {
            background: #FFD700;
            color: #0a0a0f;
            padding: 15px 40px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 10px;
            font-weight: bold;
        }

        .btn-gold:hover {
            background: #e6c200;
        }

        .btn-dark {
            background: #333;
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 10px;
        }

        .btn-dark:hover {
            background: #555;
        }

        .features {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 40px 0;
            flex-wrap: wrap;
        }

        .feature {
            background: #1a1a2e;
            padding: 20px;
            border-radius: 12px;
            width: 200px;
        }

        .feature h3 {
            color: #00d4ff;
        }

        .footer {
            margin-top: 50px;
            color: #666;
            font-size: 14px;
        }

        input[type="text"] {
            padding: 15px;
            width: 60%;
            max-width: 500px;
            border-radius: 8px;
            border: 2px solid #1a1a2e;
            background: #1a1a2e;
            color: white;
            font-size: 16px;
        }

        input[type="text"]:focus {
            border-color: #00d4ff;
            outline: none;
        }
    </style>

</head>

<body>

<h1>🔧 IT Pro - Assistant IT</h1>

<p style="font-size:20px;color:#aaa;">
Diagnostics informatiques & abonnements Pro/Business
</p>

<div style="margin:30px 0;">
    <input
        type="text"
        placeholder="Décrivez votre problème..."
        id="search">

    <br><br>

    <button class="btn" onclick="search()">
        🔍 Rechercher
    </button>
</div>

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

<div style="margin:40px 0;">

<a href="https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/" class="btn">
🚀 Accéder à l'application
</a>

<a href="https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/Offres" class="btn-gold">
💳 Voir les offres / Payer
</a>

<a href="https://github.com/vanschoor-stephanie/moteur-de-recherche-IT" class="btn-dark">
🐙 Voir sur GitHub
</a>

</div>

<div class="footer">
    <p>IT Pro - Par Stéphanie Vanschoor</p>
    <p style="font-size:12px;">Version 2.0 - 2026</p>
</div>

<script>
function search() {
    var query = document.getElementById("search").value;

    if(query.trim() !== ""){
        window.location.href =
        "https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/?q="
        + encodeURIComponent(query);
    }
}
</script>

</body>
</html>
"""

st.markdown(html, unsafe_allow_html=True)
