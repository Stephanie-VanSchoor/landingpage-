import streamlit as st
import sqlite3
import pandas as pd
import re
from datetime import datetime, date, timedelta
import hashlib
import random
import string
from io import BytesIO
import textwrap
import os

# ==================================================
# CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Assistant IT Pro - Premium",
    page_icon="💻",
    layout="wide"
)

DB = "assistant_it_pro.db"

# ==================================================
# CSS
# ==================================================

st.markdown("""
<style>
    .stApp { background-color: #0a0a0f; }
    h1, h2, h3 { color: #00d4ff !important; }
    p, li, label { color: #ffffff !important; }

    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0077be 100%) !important;
        color: #0a0a0f !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 30px !important;
    }
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 30px #00d4ff40 !important;
    }

    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background: #1a1a2e !important;
        border: 2px solid #2a2a4a !important;
        border-radius: 12px !important;
        color: white !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #00d4ff !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATE
# ==================================================

if "user" not in st.session_state:
    st.session_state.user = None
if "premium" not in st.session_state:
    st.session_state.premium = False
if "plan" not in st.session_state:
    st.session_state.plan = "gratuit"
if "recherches" not in st.session_state:
    st.session_state.recherches = 0
if "recherches_jour" not in st.session_state:
    st.session_state.recherches_jour = 0
if "date_recherche" not in st.session_state:
    st.session_state.date_recherche = date.today()
if "page" not in st.session_state:
    st.session_state.page = "accueil"
if "moteur" not in st.session_state:
    st.session_state.moteur = None
if "montant_virement" not in st.session_state:
    st.session_state.montant_virement = 0
if "offre_virement" not in st.session_state:
    st.session_state.offre_virement = ""
if "plan_virement" not in st.session_state:
    st.session_state.plan_virement = ""
if "ref_virement" not in st.session_state:
    st.session_state.ref_virement = ""

# ==================================================
# OFFRES
# ==================================================

OFFRES = {
    "gratuit": {
        "nom": "Gratuit",
        "prix": "0€",
        "recherches": 3,
        "features": ["3 recherches par jour", "70+ diagnostics", "Diagnostics basiques"]
    },
    "pro": {
        "nom": "Pro",
        "prix": "9.90€/mois",
        "recherches": 999,
        "features": ["Recherches illimitées", "150+ diagnostics", "Diagnostics avancés", "Export PDF",
                     "Support prioritaire"]
    },
    "business": {
        "nom": "Business",
        "prix": "29.90€/mois",
        "recherches": 9999,
        "features": ["Recherches illimitées", "150+ diagnostics", "Diagnostics experts", "Export PDF/Word",
                     "Support 24/7", "Accès API", "5 comptes inclus"]
    }
}

# ==================================================
# BASE DE DONNEES
# ==================================================

def connexion_db():
    return sqlite3.connect(DB)

def creer_base():
    conn = connexion_db()
    cur = conn.cursor()
    
    # Table pannes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pannes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT,
            description TEXT,
            diagnostic TEXT,
            procedure TEXT,
            questions TEXT,
            categorie TEXT,
            niveau INTEGER,
            tags TEXT
        )
    """)
    
    # Table entreprises
    cur.execute("""
        CREATE TABLE IF NOT EXISTS entreprises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            date_creation TEXT,
            plan TEXT DEFAULT 'business'
        )
    """)
    
    # Table utilisateurs (avec abonnement_expire_le)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            plan TEXT DEFAULT 'gratuit',
            premium INTEGER DEFAULT 0,
            recherches INTEGER DEFAULT 0,
            date_inscription TEXT,
            entreprise_id INTEGER,
            role TEXT DEFAULT 'membre',
            abonnement_expire_le TEXT,
            FOREIGN KEY (entreprise_id) REFERENCES entreprises (id)
        )
    """)
    
    # Table invitations
    cur.execute("""
        CREATE TABLE IF NOT EXISTS invitations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            token TEXT UNIQUE,
            entreprise_id INTEGER,
            date_creation TEXT,
            expire_le TEXT,
            FOREIGN KEY (entreprise_id) REFERENCES entreprises (id)
        )
    """)
    
    conn.commit()
    
    # Pour les bases existantes
    try:
        cur.execute("ALTER TABLE utilisateurs ADD COLUMN abonnement_expire_le TEXT")
    except:
        pass
    
    conn.close()

def remplir_base():
    conn = connexion_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM pannes")
    if cur.fetchone()[0] == 0:
        donnees = [
            ("Windows ne s'installe pas", "L'installation de Windows échoue",
             "Problème de clé USB ou de pilote manquant",
             "1- Vérifier la clé USB\n2- Désactiver Secure Boot\n3- Installer les pilotes manuellement",
             "Quelle version de Windows ?", "Windows", 4, "installation,windows"),
        ]
        cur.executemany(
            "INSERT INTO pannes (titre, description, diagnostic, procedure, questions, categorie, niveau, tags) VALUES (?,?,?,?,?,?,?,?)",
            donnees
        )
    conn.commit()
    conn.close()

# ==================================================
# MOTEUR DE RECHERCHE
# ==================================================

class RechercheIT:
    def __init__(self):
        self.df = None

    def charger(self):
        if self.df is None:
            conn = connexion_db()
            self.df = pd.read_sql_query("SELECT * FROM pannes", conn)
            conn.close()

    def rechercher(self, question):
        self.charger()
        question = question.lower()
        mots = re.findall(r"\w+", question)
        resultats = []
        for _, panne in self.df.iterrows():
            score = 0
            champs = f"{panne['titre']} {panne['description']} {panne['tags']} {panne['categorie']}".lower()
            for mot in mots:
                if len(mot) > 1 and mot in champs:
                    score += 5
                if mot in panne['titre'].lower():
                    score += 10
            if score > 0:
                resultats.append((dict(panne), score))
        resultats.sort(key=lambda x: x[1], reverse=True)
        return resultats[:10]

# ==================================================
# FONCTIONS D'EXPORT
# ==================================================

def generer_pdf_resultats(resultats, question):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import simpleSplit
        from io import BytesIO
    except ImportError:
        st.error("❌ La bibliothèque 'reportlab' n'est pas installée.")
        return None

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largeur, hauteur = A4
    y = hauteur - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Résultats de recherche - Assistant IT Pro")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Question posée : {question}")
    y -= 20
    c.drawString(50, y, f"{len(resultats)} résultat(s) trouvé(s)")
    y -= 30

    for i, (panne, score) in enumerate(resultats, 1):
        if y < 100:
            c.showPage()
            y = hauteur - 50
            c.setFont("Helvetica", 12)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"{i}. {panne['titre']} (Score: {score})")
        y -= 20
        c.setFont("Helvetica", 10)
        texte = f"Catégorie : {panne['categorie']}"
        c.drawString(60, y, texte)
        y -= 15
        texte = f"Diagnostic : {panne['diagnostic']}"
        for ligne in simpleSplit(texte, "Helvetica", 10, largeur - 100):
            c.drawString(60, y, ligne)
            y -= 15
        texte = f"Procédure : {panne['procedure']}"
        for ligne in simpleSplit(texte, "Helvetica", 10, largeur - 100):
            c.drawString(60, y, ligne)
            y -= 15
        if panne.get('questions'):
            c.drawString(60, y, f"Questions : {panne['questions']}")
            y -= 15
        y -= 10

    c.save()
    return buffer.getvalue()

def generer_word_resultats(resultats, question):
    try:
        import docx
        from docx.shared import Pt
        from io import BytesIO
    except ImportError:
        st.error("❌ La bibliothèque 'python-docx' n'est pas installée.")
        return None

    doc = docx.Document()
    doc.add_heading("Résultats de recherche - Assistant IT Pro", 0)
    doc.add_paragraph(f"Question posée : {question}")
    doc.add_paragraph(f"{len(resultats)} résultat(s) trouvé(s)")
    doc.add_paragraph()

    for i, (panne, score) in enumerate(resultats, 1):
        doc.add_heading(f"{i}. {panne['titre']} (Score: {score})", level=1)
        p = doc.add_paragraph()
        p.add_run("Catégorie : ").bold = True
        p.add_run(panne['categorie'])
        p = doc.add_paragraph()
        p.add_run("Diagnostic : ").bold = True
        p.add_run(panne['diagnostic'])
        p = doc.add_paragraph()
        p.add_run("Procédure : ").bold = True
        p.add_run(panne['procedure'])
        if panne.get('questions'):
            p = doc.add_paragraph()
            p.add_run("Questions : ").bold = True
            p.add_run(panne['questions'])
        doc.add_paragraph()

    buffer = BytesIO()
    doc.save(buffer)
    return buffer.getvalue()

# ==================================================
# GESTION D'ENTREPRISE
# ==================================================

def creer_entreprise(email_admin, nom_entreprise):
    conn = connexion_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO entreprises (nom, date_creation, plan) VALUES (?, ?, 'business')",
            (nom_entreprise, date.today().isoformat())
        )
        entreprise_id = cur.lastrowid
        cur.execute(
            "UPDATE utilisateurs SET entreprise_id = ?, role = 'admin' WHERE email = ?",
            (entreprise_id, email_admin)
        )
        conn.commit()
        conn.close()
        return entreprise_id
    except:
        conn.close()
        return None

def get_entreprise_id(email):
    conn = connexion_db()
    cur = conn.cursor()
    cur.execute("SELECT entreprise_id FROM utilisateurs WHERE email = ?", (email,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def get_membres(entreprise_id):
    conn = connexion_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT email, role, date_inscription FROM utilisateurs WHERE entreprise_id = ?",
        (entreprise_id,)
    )
    membres = cur.fetchall()
    conn.close()
    return membres

def get_nb_membres(entreprise_id):
    conn = connexion_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM utilisateurs WHERE entreprise_id = ?", (entreprise_id,))
    count = cur.fetchone()[0]
    conn.close()
    return count

def get_recherches_entreprise(entreprise_id):
    conn = connexion_db()
    cur = conn.cursor()
    cur.execute("SELECT SUM(recherches) FROM utilisateurs WHERE entreprise_id = ?", (entreprise_id,))
    total = cur.fetchone()[0]
    conn.close()
    return total if total else 0

def generer_token_invitation():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))

def creer_invitation(email_invite, entreprise_id):
    if get_nb_membres(entreprise_id) >= 5:
        return None, "❌ Limite de 5 comptes atteinte"
    
    conn = connexion_db()
    cur = conn.cursor()
    token = generer_token_invitation()
    expire_le = (datetime.now() + timedelta(days=7)).isoformat()
    try:
        cur.execute(
            "INSERT INTO invitations (email, token, entreprise_id, date_creation, expire_le) VALUES (?, ?, ?, ?, ?)",
            (email_invite, token, entreprise_id, date.today().isoformat(), expire_le)
        )
        conn.commit()
        conn.close()
        return token, None
    except:
        conn.close()
        return None, "❌ Erreur lors de la création de l'invitation"

def verifier_invitation(token):
    conn = connexion_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT email, entreprise_id FROM invitations WHERE token = ? AND expire_le > ?",
        (token, date.today().isoformat())
    )
    result = cur.fetchone()
    conn.close()
    return result

def utiliser_invitation(token):
    conn = connexion_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM invitations WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def est_admin(email):
    conn = connexion_db()
    cur = conn.cursor()
    cur.execute("SELECT role FROM utilisateurs WHERE email = ?", (email,))
    result = cur.fetchone()
    conn.close()
    return result and result[0] == "admin"

# ==================================================
# AUTHENTIFICATION
# ==================================================

def inscription(email, password):
    conn = connexion_db()
    cur = conn.cursor()
    try:
        pwd = hashlib.sha256(password.encode()).hexdigest()
        cur.execute(
            "INSERT INTO utilisateurs (email, password, plan, premium, recherches, date_inscription) VALUES (?, ?, 'gratuit', 0, 0, ?)",
            (email, pwd, date.today().isoformat())
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def connexion_utilisateur(email, password):
    conn = connexion_db()
    cur = conn.cursor()
    pwd = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("SELECT * FROM utilisateurs WHERE email = ? AND password = ?", (email, pwd))
    user = cur.fetchone()
    return user

def mise_a_jour_plan(email, plan):
    conn = connexion_db()
    cur = conn.cursor()
    
    cur.execute("UPDATE utilisateurs SET plan = ?, premium = 1 WHERE email = ?", (plan, email))
    
    if plan == "business":
        cur.execute("SELECT entreprise_id FROM utilisateurs WHERE email = ?", (email,))
        result = cur.fetchone()
        if result and result[0] is None:
            nom_entreprise = f"Entreprise de {email}"
            cur.execute(
                "INSERT INTO entreprises (nom, date_creation, plan) VALUES (?, ?, 'business')",
                (nom_entreprise, date.today().isoformat())
            )
            entreprise_id = cur.lastrowid
            cur.execute(
                "UPDATE utilisateurs SET entreprise_id = ?, role = 'admin' WHERE email = ?",
                (entreprise_id, email)
            )
    
    conn.commit()
    conn.close()

# ==================================================
# PAGES
# ==================================================

def page_offres():
    st.markdown(
        '<p style="color:#FFD700; font-size:36px; font-weight:700; text-align:center;">📋 Nos Offres</p>',
        unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 15px; border: 1px solid #2a2a4a; text-align: center;'>
            <h3 style='color: #aaa;'>🆓 Gratuit</h3>
            <p style='font-size: 28px; color: white;'>0€</p>
            <hr>
            <p style='color: #ccc;'>✅ 3 recherches / jour</p>
            <p style='color: #ccc;'>✅ 70+ diagnostics</p>
            <p style='color: #ccc;'>✅ Diagnostics basiques</p>
            <br>
            <span style='background: #2a2a4a; padding: 8px 20px; border-radius: 50px; color: #aaa;'>Actuel</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 15px; border: 2px solid #FFD700; text-align: center;'>
            <h3 style='color: #FFD700;'>🚀 Pro</h3>
            <p style='font-size: 28px; color: white;'>9.90€<span style='font-size: 16px; color: #aaa;'> /mois</span></p>
            <hr>
            <p style='color: #ccc;'>✅ Recherches illimitées</p>
            <p style='color: #ccc;'>✅ 150+ diagnostics</p>
            <p style='color: #ccc;'>✅ Diagnostics avancés</p>
            <p style='color: #ccc;'>✅ Export PDF</p>
            <p style='color: #ccc;'>✅ Support prioritaire</p>
            <br>
        """, unsafe_allow_html=True)
        if st.button("Choisir Pro", type="primary", key="offre_pro"):
            st.session_state.montant_virement = 9.90
            st.session_state.offre_virement = "Pro"
            st.session_state.plan_virement = "pro"
            st.session_state.page = "💳 Virement"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 15px; border: 2px solid #9B59B6; text-align: center;'>
            <h3 style='color: #9B59B6;'>🏢 Business</h3>
            <p style='font-size: 28px; color: white;'>29.90€<span style='font-size: 16px; color: #aaa;'> /mois</span></p>
            <hr>
            <p style='color: #ccc;'>✅ Tout Pro inclus</p>
            <p style='color: #ccc;'>✅ Diagnostics experts</p>
            <p style='color: #ccc;'>✅ Export PDF/Word</p>
            <p style='color: #ccc;'>✅ Support 24/7</p>
            <p style='color: #ccc;'>✅ Accès API</p>
            <p style='color: #ccc;'>✅ 5 comptes inclus</p>
            <br>
        """, unsafe_allow_html=True)
        if st.button("Choisir Business", type="primary", key="offre_business"):
            st.session_state.montant_virement = 29.90
            st.session_state.offre_virement = "Business"
            st.session_state.plan_virement = "business"
            st.session_state.page = "💳 Virement"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.info("💡 Les offres Pro et Business sont **sans engagement** et peuvent être résiliées à tout moment.")

def page_virement():
    st.markdown(
        '<p style="color:#FFD700; font-size:36px; font-weight:700; text-align:center;">💳 Paiement par Virement Bancaire</p>',
        unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a5276 0%, #2e86c1 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px;'>
        <h2 style='color: white;'>Paiement sécurisé</h2>
        <p style='color: #FFD700;'>Virement bancaire - 0€ de frais</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Choisissez votre offre")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("""
            ### 🚀 PRO
            **9.90€ / mois** | **79€ / an**
            - Recherches illimitées
            - Diagnostics avancés
            - 150+ diagnostics
            - Export PDF
            - Support prioritaire
            - Statistiques avancées
            """)
            if st.button("Choisir Pro - 9.90€", type="primary", use_container_width=True):
                st.session_state.montant_virement = 9.90
                st.session_state.offre_virement = "Pro"
                st.session_state.plan_virement = "pro"
                st.success("✅ Offre Pro sélectionnée !")
                st.balloons()

    with col2:
        with st.container(border=True):
            st.markdown("""
            ### 🏢 BUSINESS
            **29.90€ / mois** | **249€ / an**
            - Tout Pro inclus
            - Diagnostics experts
            - 150+ diagnostics
            - Export PDF/Word
            - Support 24/7
            - Accès API
            - 5 comptes inclus
            """)
            if st.button("Choisir Business - 29.90€", type="primary", use_container_width=True):
                st.session_state.montant_virement = 29.90
                st.session_state.offre_virement = "Business"
                st.session_state.plan_virement = "business"
                st.success("✅ Offre Business sélectionnée !")
                st.balloons()

    if st.session_state.montant_virement > 0:
        st.markdown("---")
        st.markdown("### Effectuez le virement")

        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        st.session_state.ref_virement = ref

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; border: 1px solid #2a2a4a;'>
                <h4 style='color: #00d4ff;'>Coordonnées bancaires</h4>
                <p><strong style='color:#aaa;'>Titulaire :</strong> <span style='color:white;'>IT Pro Solutions</span></p>
                <p><strong style='color:#aaa;'>IBAN :</strong> <span style='color:white;'>BE80 9733 8252 3877</span></p>
                <p><strong style='color:#aaa;'>BIC :</strong> <span style='color:white;'>ARSPBE22XXX</span></p>
                <p><strong style='color:#aaa;'>Banque :</strong> <span style='color:white;'>ARGENTA</span></p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; border: 1px solid #2ecc71;'>
                <h4 style='color: #2ecc71;'>Informations importantes</h4>
                <p><strong style='color:#aaa;'>Montant :</strong> <span style='color:#00d4ff;font-weight:700;'>{st.session_state.montant_virement}€</span></p>
                <p><strong style='color:#aaa;'>Offre :</strong> <span style='color:#FFD700;'>{st.session_state.offre_virement}</span></p>
                <p><strong style='color:#aaa;'>Référence :</strong> <code style='background:#0a0a0f;color:#00d4ff;padding:2px 8px;border-radius:4px;'>{ref}</code></p>
                <p><strong style='color:#aaa;'>Email :</strong> <span style='color:white;'>tech.contactinformatique@proton.me</span></p>
                <p style='color: #e74c3c; font-weight:700;'>⚠️ Indiquez la référence dans le libellé</p>
            </div>
            """, unsafe_allow_html=True)

        st.info(f"""
        **📋 Résumé du virement :**
        - Montant : {st.session_state.montant_virement}€
        - Offre : {st.session_state.offre_virement}
        - Référence : {ref}
        - Email : tech.contactinformatique@proton.me
        - Délai : 24-48h ouvrés
        """)
        st.warning(
            "⏳ Après le virement, votre compte sera activé sous 24-48h ouvrés. Un email de confirmation vous sera envoyé.")

def page_licence():
    st.markdown(
        '<p style="color:#FFD700; font-size:36px; font-weight:700; text-align:center;">📄 Licence et Mentions légales</p>',
        unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    ### 📌 Propriété intellectuelle
    - Tous les droits de propriété intellectuelle sur le logiciel **Assistant IT Pro** appartiennent à **IT Pro Solutions**.
    - Toute reproduction, modification ou distribution sans autorisation est interdite.

    ### 🔒 Protection des données
    - Les données utilisateur sont stockées de manière sécurisée et ne sont jamais partagées avec des tiers.
    - Conformément au RGPD, vous pouvez demander la suppression de vos données à tout moment.

    ### 💰 Paiements
    - Les paiements sont traités par virement bancaire. Aucune carte bancaire n'est stockée sur nos serveurs.
    - Les abonnements sont sans engagement et peuvent être résiliés en nous contactant.

    ### 📞 Support
    - Contact : tech.contactinformatique@proton.me
    - Délai de réponse : 24-48h ouvrés

    ---
    *Version 2.0 – 2026*
    """)

def page_landing():
    st.markdown("""
    <style>
        .big-title { font-size: 48px; color: #00d4ff; text-align: center; }
        .subtitle { font-size: 20px; color: #aaa; text-align: center; }
        .feature-box { background: #1a1a2e; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #2a2a4a; margin: 10px; }
        .btn-landing { 
            background: #00d4ff; color: #0a0a0f; padding: 15px 40px; 
            border: none; border-radius: 10px; font-size: 18px; font-weight: 700; 
            cursor: pointer; text-decoration: none; display: inline-block; 
            margin: 10px; 
        }
        .btn-landing:hover { background: #00b8e6; }
    </style>
    <div class="big-title">🔧 IT Pro</div>
    <div class="subtitle">Assistant IT – Diagnostics &amp; Abonnements</div>
    <br>
    <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
        <div class="feature-box"><h3>⚡ Rapide</h3><p>Résultats en 0,5 seconde</p></div>
        <div class="feature-box"><h3>🔒 Sécurisé</h3><p>Mots de passe hachés</p></div>
        <div class="feature-box"><h3>📊 1000+ diagnostics</h3><p>Base complète</p></div>
    </div>
    """, unsafe_allow_html=True)

def page_equipe():
    st.markdown(
        '<p style="color:#FFD700; font-size:36px; font-weight:700; text-align:center;">👥 Gestion d\'équipe</p>',
        unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state.user:
        st.error("❌ Connectez-vous d'abord")
        return
    
    entreprise_id = get_entreprise_id(st.session_state.user)
    
    if not entreprise_id:
        st.info("🏢 Vous n'avez pas encore d'équipe.")
        if st.session_state.plan == "business":
            st.markdown("### Créer votre entreprise")
            nom_entreprise = st.text_input("Nom de l'entreprise", placeholder="Ex: IT Pro Solutions")
            if st.button("🏢 Créer mon entreprise", type="primary"):
                if nom_entreprise:
                    new_id = creer_entreprise(st.session_state.user, nom_entreprise)
                    if new_id:
                        st.success(f"✅ Entreprise '{nom_entreprise}' créée !")
                        st.rerun()
                    else:
                        st.error("❌ Erreur lors de la création")
                else:
                    st.warning("⚠️ Veuillez entrer un nom")
        else:
            st.info("💡 Passez à l'offre **Business** pour créer une équipe (5 comptes inclus).")
        return
    
    if not est_admin(st.session_state.user):
        st.markdown("### 📊 Votre équipe")
        membres = get_membres(entreprise_id)
        for email, role, date_ins in membres:
            st.markdown(f"- **{email}** ({'👑 Admin' if role == 'admin' else '👤 Membre'})")
        total_rech = get_recherches_entreprise(entreprise_id)
        st.info(f"🔍 Recherches totales de l'équipe : {total_rech}")
        return
    
    conn = connexion_db()
    cur = conn.cursor()
    cur.execute("SELECT nom, date_creation FROM entreprises WHERE id = ?", (entreprise_id,))
    entreprise = cur.fetchone()
    conn.close()
    
    if entreprise:
        st.markdown(f"### 🏢 {entreprise[0]}")
        st.markdown(f"*Créée le : {entreprise[1]}*")
    
    st.markdown("---")
    st.markdown("### 📋 Membres de l'équipe")
    membres = get_membres(entreprise_id)
    
    for email, role, date_ins in membres:
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.markdown(f"**{email}** ({'👑 Admin' if role == 'admin' else '👤 Membre'})")
        with col2:
            st.markdown(f"*Inscrit le {date_ins}*")
        with col3:
            if role != "admin":
                if st.button(f"❌", key=f"del_{email}"):
                    conn = connexion_db()
                    cur = conn.cursor()
                    cur.execute(
                        "UPDATE utilisateurs SET entreprise_id = NULL, plan = 'gratuit', premium = 0 WHERE email = ?",
                        (email,)
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"✅ {email} a été retiré de l'équipe")
                    st.rerun()
    
    nb_membres = len(membres)
    st.progress(nb_membres / 5)
    st.markdown(f"**{nb_membres}/5** comptes utilisés")
    
    st.markdown("---")
    st.markdown("### 📧 Inviter un nouveau membre")
    
    if nb_membres >= 5:
        st.error("❌ Limite de 5 comptes atteinte")
    else:
        email_invite = st.text_input("Email à inviter", placeholder="collegue@email.com")
        if st.button("📨 Envoyer l'invitation", type="primary"):
            if email_invite and "@" in email_invite:
                membres_emails = [m[0] for m in membres]
                if email_invite in membres_emails:
                    st.warning("⚠️ Cet email est déjà dans l'équipe")
                else:
                    token, erreur = creer_invitation(email_invite, entreprise_id)
                    if token:
                        lien_invitation = f"https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/?token={token}"
                        st.success(f"✅ Invitation créée !")
                        st.info(f"🔗 Lien d'invitation :")
                        st.code(lien_invitation, language="text")
                        st.caption(f"📧 Envoyez ce lien à {email_invite}")
                    else:
                        st.error(erreur)
            else:
                st.warning("⚠️ Veuillez entrer un email valide")
    
    st.markdown("---")
    total_rech = get_recherches_
