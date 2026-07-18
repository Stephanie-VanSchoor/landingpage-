from http.server import HTTPServer, BaseHTTPRequestHandler


class LandingPageHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        html = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>IT Pro - Assistant IT</title>

<style>

body{
    font-family:Arial,sans-serif;
    text-align:center;
    padding:50px;
    background:#0a0a0f;
    color:white;
}

h1{
    font-size:48px;
    color:#00d4ff;
}

.subtitle{
    font-size:20px;
    color:#aaa;
}

.search{
    margin:30px 0;
}

input[type=text]{
    width:60%;
    max-width:500px;
    padding:15px;
    border-radius:8px;
    border:2px solid #1a1a2e;
    background:#1a1a2e;
    color:white;
    font-size:16px;
}

input[type=text]:focus{
    border-color:#00d4ff;
    outline:none;
}

.btn{
    background:#00d4ff;
    color:#000;
    padding:15px 40px;
    border-radius:8px;
    text-decoration:none;
    display:inline-block;
    margin:10px;
    font-size:18px;
    font-weight:bold;
}

.btn:hover{
    background:#00b8e6;
}

.btn-gold{
    background:#FFD700;
    color:black;
    padding:15px 40px;
    border-radius:8px;
    text-decoration:none;
    display:inline-block;
    margin:10px;
    font-size:18px;
    font-weight:bold;
}

.btn-gold:hover{
    background:#e6c200;
}

.btn-dark{
    background:#333;
    color:white;
    padding:15px 40px;
    border-radius:8px;
    text-decoration:none;
    display:inline-block;
    margin:10px;
}

.btn-dark:hover{
    background:#555;
}

.features{
    display:flex;
    justify-content:center;
    gap:30px;
    flex-wrap:wrap;
    margin:40px 0;
}

.feature{
    width:200px;
    background:#1a1a2e;
    padding:20px;
    border-radius:12px;
}

.feature h3{
    color:#00d4ff;
}

.footer{
    margin-top:60px;
    color:#666;
}

</style>

</head>

<body>

<h1>🔧 IT Pro - Assistant IT</h1>

<p class="subtitle">
Diagnostics informatiques • Solutions • Abonnements
</p>

<div class="search">

<input
id="search"
type="text"
placeholder="Décrivez votre problème...">

<br><br>

<button class="btn" onclick="search()">
🔍 Rechercher
</button>

</div>

<div class="features">

<div class="feature">
<h3>⚡ Rapide</h3>
<p>Résultats en moins d'une seconde.</p>
</div>

<div class="feature">
<h3>🔒 Sécurisé</h3>
<p>Mots de passe protégés.</p>
</div>

<div class="feature">
<h3>📊 1000+ diagnostics</h3>
<p>Base de connaissances complète.</p>
</div>

</div>

<div>

<a class="btn"
href="https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/">
🚀 Accéder à l'application
</a>

<a class="btn-gold"
href="https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/Offres">
💳 Voir les offres
</a>

<a class="btn-dark"
href="https://github.com/vanschoor-stephanie/moteur-de-recherche-IT">
🐙 GitHub
</a>

</div>

<div class="footer">
IT Pro • Stéphanie Vanschoor<br>
Version 2.0 • 2026
</div>

<script>

function search(){

    var q=document.getElementById("search").value;

    if(q.trim()!=""){

        window.location.href=
        "https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/?q="
        +encodeURIComponent(q);

    }

}

</script>

</body>
</html>
"""

        self.wfile.write(html.encode("utf-8"))


if __name__ == "__main__":

    PORT = 8000

    server = HTTPServer(("0.0.0.0", PORT), LandingPageHandler)

    print(f"🚀 Landing Page disponible sur : http://localhost:{PORT}")

    server.serve_forever()
