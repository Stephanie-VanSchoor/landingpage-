# 🔧 Assistant IT Pro - SaaS de Diagnostic Informatique

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/vanschoor-stephanie/moteur-de-recherche-IT)

> **Une application SaaS complète de diagnostics informatiques avec abonnements Pro/Business, export PDF/Word, API REST et gestion d'équipe.**

---

## 🚀 Accès à l'application

👉 **[Lien vers l'application en ligne](https://moteur-de-recherche-it-mzztfdhtggde7omb8uhzek.streamlit.app/)**

---

## 📋 Fonctionnalités

### 🔐 Authentification
- Inscription / Connexion sécurisée
- Hachage des mots de passe (SHA-256)
- Gestion des sessions utilisateur

### 💳 Système d'abonnement
| Offre | Prix | Fonctionnalités |
| :--- | :--- | :--- |
| **Gratuit** | 0€ | 3 recherches/jour, 70+ diagnostics |
| **Pro** | 9.90€/mois | Recherches illimitées, 150+ diagnostics, Export PDF |
| **Business** | 29.90€/mois | Tout Pro + Export Word, API, 5 comptes inclus |

- Paiement par virement bancaire (coordonnées affichées dans l'application)
- Expiration automatique après 30 jours

### 🔍 Moteur de recherche
- Moteur de recherche sémantique avec scoring
- 1000+ diagnostics pré-remplis
- Catégories : Windows, Linux, MacOS, Réseau, Sécurité, Matériel, etc.

### 📄 Export de rapports
- Export PDF (réservé aux abonnés Pro/Business)
- Export Word (réservé aux abonnés Business)

### 👥 Gestion d'équipe (Business)
- Création d'entreprise automatique
- Invitation de membres (5 comptes inclus)
- Rôles Admin / Membre
- Statistiques des recherches par entreprise

### ⚙️ API REST (Business)
- Endpoints : `/login`, `/rechercher`, `/diagnostic/{id}`, `/categories`, `/statistiques`
- Authentification JWT
- Accès réservé aux comptes Business

---

## 🛠️ Stack Technique

| Couche | Technologie |
| :--- | :--- |
| **Frontend** | Streamlit |
| **Backend API** | FastAPI |
| **Base de données** | SQLite |
| **Authentification** | SHA-256 + JWT |
| **Exports** | ReportLab (PDF), python-docx (Word) |
| **Déploiement** | Streamlit Cloud / GitHub |

---

## 📁 Structure du Projet
