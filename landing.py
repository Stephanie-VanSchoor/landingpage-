from http.server import HTTPServer, BaseHTTPRequestHandler

class LandingPageHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>IT Pro - Assistant IT</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }

                body {
                    font-family: 'Arial', sans-serif;
                    text-align: center;
                    padding: 50px 20px;
                    background: #0a0a0f;
                    color: white;
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }

                h1 {
                    font-size: 52px;
                    color: #00d4ff;
                    margin-bottom: 10px;
                }

                .subtitle {
                    font-size: 20px;
                    color: #aaa;
                    margin-bottom: 30px;
                }

                .search-container {
                    margin: 30px 0;
                    width: 100%;
                    max-width: 600px;
                }

                .search-container input[type="text"] {
                    padding: 16px 20px;
                    width: 100%;
                    border-radius: 10px;
                    border: 2px solid #1a1a2e;
                    background: #1a1a2e;
                    color: white;
                    font-size: 16px;
                    outline: none;
                    transition: border-color 0.3s ease;
                }

                .search-container input[type="text"]:focus {
                    border-color: #00d4ff;
                }

                .search-container button {
                    margin-top: 15px;
                }

                .btn {
                    background: #00d4ff;
                    color: #0a0a0f;
                    padding: 15px 40px;
                    border: none;
                    border-radius: 10px;
                    font-size: 18px;
                    font-weight: 700;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    margin: 8px;
                    transition: transform 0.2s ease, background 0.2s ease;
                }

                .btn:hover {
                    background: #00b8e6;
                    transform: scale(1.03);
                }

                .btn-gold {
                    background: #FFD700;
                    color: #0a0a0f;
                    padding: 15px 40px;
                    border: none;
                    border-radius: 10px;
                    font-size: 18px;
                    font-weight: 700;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    margin: 8px;
                    transition: transform 0.2s ease, background 0.2s ease;
                }

                .btn-gold:hover {
                    background: #e6c200;
                    transform: scale(1.03);
                }

                .btn-dark {
                    background: #333;
                    color: white;
                    padding: 15px 40px;
                    border: none;
                    border-radius: 10px;
                    font-size: 18px;
                    font-weight: 700;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    margin: 8px;
                    transition: transform 0.2s ease, background 0.2s ease;
                }

                .btn-dark:hover {
                    background: #555;
                    transform: scale(1.03);
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
                    padding: 25px 20px;
                    border-radius: 14px;
                    width: 200px;
                    border: 1px solid #2a2a4a;
                    transition: transform 0.2s ease, border-color 0.2s ease;
                }

                .feature:hover {
                    transform: translateY(-5px);
                    border-color: #00d4ff;
                }

                .feature h3 {
                    color: #00d4ff;
                    font-size: 22px;
                    margin-bottom: 8px;
                }

                .feature p {
                    color: #bbb;
                    font-size: 15px;
                }

                .footer {
                    margin-top: 50px;
                    color: #555;
                    font-size: 14px;
                    line-height: 1.8;
                }

                .footer a {
                    color: #00d4ff;
                    text-decoration: none;
                }

                .footer a:hover {
                    text-decoration: underline;
                }

                @media (max-width: 700px) {
                    h1 { font-size: 32px; }
                    .subtitle { font-size: 16px; }
                    .features { gap: 15px; }
                    .feature { width: 160px; padding: 18px 12px; }
                    .btn, .btn-gold, .btn-dark {
                        padding: 12px 25px;
                        font-size: 15px;
                        display: block;
                        margin: 10px auto;
                        width: 80%;
                        max-width: 280px;
                    }
                }

                @media (max-width: 450px) {
                    h1 { font-size: 26px; }
                    .feature { width: 100%; max-width: 280px; }
                    .search-container input[type="text"] { font-size: 14px; padding: 14px 16px; }
                }
            </style>
        </head>
        <body>

            <!-- ===== TITRE ===== -->
            <h1>🔧 IT Pro</h1>
            <p class="subtitle">Assistant IT – Diagnostics &amp; Abonnements</p>

            <!-- ===== BARRE DE RECHERCHE ===== -->
            <div class="search-container">
                <input type="text" id="search" placeholder="Décrivez votre problème (ex: PC lent, wifi...)">
                <br>
                <button class="btn" onclick="search()">🔍 Rechercher</button>
            </div>

            <!-- ===== FONCTIONNALITÉS ===== -->
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

            <!-- ===== BOUTONS ===== -->
            <div style="margin: 30px 0;">
                <a href="https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/"
                   class="btn" target="_blank">
                   🚀 Accéder à l'application
                </a>

                <a href="https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/Offres"
                   class="btn-gold" target="_blank">
                   💳 Voir les offres / Payer
                </a>

                <a href="https://github.com/vanschoor-stephanie/moteur-de-recherche-IT"
                   class="btn-dark" target="_blank">
                   🐙 Voir sur GitHub
                </a>
            </div>

            <!-- ===== PIED DE PAGE ===== -->
            <div class="footer">
                <p>IT Pro – Par <strong>Stéphanie Vanschoor</strong></p>
                <p style="font-size: 12px;">Version 2.0 – 2026 &nbsp;|&nbsp;
                    <a href="https://github.com/vanschoor-stephanie/moteur-de-recherche-IT" target="_blank">GitHub</a>
                </p>
            </div>

            <script>
                function search() {
                    var query = document.getElementById('search').value;
                    if (query.trim() !== '') {
                        window.location.href =
                            'https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/?q=' +
                            encodeURIComponent(query);
                    } else {
                        alert('Veuillez entrer une description de votre problème.');
                    }
                }

                document.addEventListener('DOMContentLoaded', function() {
                    document.getElementById('search').addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') {
                            search();
                        }
                    });
                });
            </script>

        </body>
        </html>
        """

        self.wfile.write(html.encode('utf-8'))

if __name__ == '__main__':
    port = 8000
    server = HTTPServer(('0.0.0.0', port), LandingPageHandler)
    print(f"🚀 Serveur lancé sur http://localhost:{port}")
    print("Appuie sur Ctrl+C pour arrêter")
    server.serve_forever()
