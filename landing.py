def main():
    creer_base()
    remplir_base()

    if st.session_state.moteur is None:
        st.session_state.moteur = RechercheIT()

    if st.session_state.date_recherche != date.today():
        st.session_state.date_recherche = date.today()
        st.session_state.recherches_jour = 0

    # ==================================================
    # SIDEBAR
    # ==================================================

    with st.sidebar:
        st.markdown("""
        <style>
            section[data-testid="stSidebar"] {
                background-color: #1a1a2e !important;
            }
        </style>
        """, unsafe_allow_html=True)
        st.markdown('<p style="color:#1458; font-size:24px; font-weight:700; text-align:center;">💻 IT Pro</p>',
                    unsafe_allow_html=True)
        st.markdown('<p style="color:#AAAAAA; font-size:12px; text-align:center;">1000 diagnostics</p>',
                    unsafe_allow_html=True)
        st.markdown("---")

        if st.session_state.user:
            st.markdown(f'<p style="color:#FFFFFF;">👤 {st.session_state.user}</p>', unsafe_allow_html=True)

            plan = st.session_state.plan
            if plan == "business":
                st.markdown(
                    '<div style="background:#9B59B6; padding:12px; border-radius:10px; text-align:center;"><p style="color:white; font-weight:700; margin:0;">🏢 BUSINESS</p></div>',
                    unsafe_allow_html=True)
            elif plan == "pro":
                st.markdown(
                    '<div style="background:#FFD700; padding:12px; border-radius:10px; text-align:center;"><p style="color:#0a0a0f; font-weight:700; margin:0;">🚀 PRO</p></div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div style="background:#FF6B6B; padding:12px; border-radius:10px; text-align:center;"><p style="color:white; font-weight:700; margin:0;">🆓 GRATUIT</p></div>',
                    unsafe_allow_html=True)
                restant = max(0, 3 - st.session_state.recherches_jour)
                st.markdown(f'<p style="color:#FFFFFF;">🔍 {restant} recherches restantes</p>', unsafe_allow_html=True)
                st.progress(st.session_state.recherches_jour / 3)

            st.markdown("---")
            menu = ["🏠 Accueil", "📋 Offres", "💳 Virement", "📄 Licence"]
            
            # Ajouter "👥 Équipe" si l'utilisateur a une entreprise
            entreprise_id = get_entreprise_id(st.session_state.user) if st.session_state.user else None
            if entreprise_id:
                menu.append("👥 Équipe")
            
            st.session_state.page = st.radio("Navigation", menu, key="sidebar_menu")

            if st.button("🚪 Déconnexion", use_container_width=True):
                st.session_state.user = None
                st.session_state.premium = False
                st.session_state.plan = "gratuit"
                st.session_state.recherches = 0
                st.session_state.recherches_jour = 0
                st.rerun()
        else:
            tab1, tab2 = st.tabs(["🔐 Connexion", "📝 Inscription"])
            with tab1:
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Mot de passe", type="password", key="login_pass")
                if st.button("Se connecter", use_container_width=True):
                    user = connexion_utilisateur(email, password)
                    if user:
                        st.session_state.user = email
                        st.session_state.plan = user[3] if user[3] else "gratuit"
                        st.session_state.premium = bool(user[4])
                        st.session_state.recherches = user[5] if user[5] else 0
                        st.session_state.recherches_jour = user[5] if user[5] else 0
                        st.success("✅ Connecté !")
                        st.rerun()
                    else:
                        st.error("❌ Identifiants incorrects")
            with tab2:
                email = st.text_input("Email", key="register_email")
                password = st.text_input("Mot de passe", type="password", key="register_pass")
                token_invitation = st.text_input("🔑 Code d'invitation (optionnel)", key="token_invitation", 
                                                  placeholder="Si vous avez reçu une invitation")
                
                if st.button("Créer un compte", use_container_width=True):
                    if inscription(email, password):
                        if token_invitation:
                            invitation = verifier_invitation(token_invitation)
                            if invitation:
                                email_invite, entreprise_id = invitation
                                if email != email_invite:
                                    st.error("❌ Cette invitation est destinée à un autre email")
                                else:
                                    conn = connexion_db()
                                    cur = conn.cursor()
                                    cur.execute(
                                        "UPDATE utilisateurs SET entreprise_id = ?, plan = 'business', premium = 1 WHERE email = ?",
                                        (entreprise_id, email)
                                    )
                                    conn.commit()
                                    conn.close()
                                    utiliser_invitation(token_invitation)
                                    st.success("✅ Compte créé ! Vous avez rejoint l'équipe. Connectez-vous.")
                            else:
                                st.warning("⚠️ Code d'invitation invalide ou expiré")
                        else:
                            st.success("✅ Compte créé ! Connectez-vous")
                    else:
                        st.error("❌ Email déjà utilisé")

    # ==================================================
    # GESTION DES PAGES
    # ==================================================

    if st.session_state.page == "📋 Offres":
        page_offres()
        return
    if st.session_state.page == "💳 Virement":
        page_virement()
        return
    if st.session_state.page == "📄 Licence":
        page_licence()
        return
    if st.session_state.page == "👥 Équipe":
        page_equipe()
        return

    # ==================================================
    # ACCUEIL - AVEC LANDING PAGE
    # ==================================================

    # ========== SI L'UTILISATEUR N'EST PAS CONNECTÉ ==========
    if not st.session_state.user:
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
        
        st.info("🔐 **Connectez-vous** dans la barre latérale pour accéder à l'application.")
        
        st.markdown("""
        <div style="text-align: center; margin-top: 30px;">
            <p style="color: #aaa;">Version 2.0 – 2026</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # ========== SI L'UTILISATEUR EST CONNECTÉ ==========
    st.markdown(
        '<p style="color:#00d4ff; font-size:48px; font-weight:900; text-align:center;">🔧 Assistant Dépannage IT</p>',
        unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#aaa; text-align:center; font-size:18px;">Par IT Pro Solutions - <span style="color:#FFD700;">150+ diagnostics</span></p>',
        unsafe_allow_html=True)
    st.markdown("---")

    question = st.text_area("Décrivez votre problème :", height=100,
                            placeholder="Ex: mon PC est lent, le wifi ne marche pas, erreur Windows...")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 Rechercher", type="primary", use_container_width=True):
            if not st.session_state.user:
                st.error("❌ Connectez-vous d'abord")
            elif not st.session_state.premium and st.session_state.recherches_jour >= 3:
                st.error("🔴 LIMITE ATTEINTE ! Passez Premium pour continuer.")
                if st.button("VOIR LES OFFRES"):
                    st.session_state.page = "📋 Offres"
                    st.rerun()
            elif question.strip():
                with st.spinner("Recherche en cours..."):
                    if not st.session_state.premium:
                        st.session_state.recherches_jour += 1
                        st.session_state.recherches += 1
                    results = st.session_state.moteur.rechercher(question)
                    if results:
                        st.success(f"✅ {len(results)} résultat(s) trouvé(s)")
                        for panne, score in results:
                            with st.expander(f"🔹 {panne['titre']} (Score: {score})"):
                                st.markdown(f"**Catégorie:** {panne['categorie']}")
                                st.markdown(f"**Diagnostic:** {panne['diagnostic']}")
                                st.markdown(f"**Procédure:**\n{panne['procedure']}")
                                if panne.get('questions'):
                                    st.info(f"❓ {panne['questions']}")

                        # ========== BOUTONS D'EXPORT (RÉSERVÉS PRO/BUSINESS) ==========
                        if st.session_state.plan in ["pro", "business"]:
                            st.markdown("---")
                            col_btn1, col_btn2 = st.columns(2)
                            with col_btn1:
                                pdf_data = generer_pdf_resultats(results, question)
                                if pdf_data:
                                    st.download_button(
                                        label="📄 Télécharger en PDF",
                                        data=pdf_data,
                                        file_name=f"resultats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                        mime="application/pdf",
                                        key="pdf_download"
                                    )
                                else:
                                    st.warning("Export PDF indisponible (bibliothèque manquante)")
                            with col_btn2:
                                word_data = generer_word_resultats(results, question)
                                if word_data:
                                    st.download_button(
                                        label="📝 Télécharger en Word",
                                        data=word_data,
                                        file_name=f"resultats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                        key="word_download"
                                    )
                                else:
                                    st.warning("Export Word indisponible (bibliothèque manquante)")
                        else:
                            st.info("🔒 L'export PDF/Word est disponible uniquement pour les abonnés **Pro** et **Business**.")
                    else:
                        st.warning("😕 Aucun résultat trouvé")
            else:
                st.warning("⚠️ Décrivez votre problème")

    st.markdown("---")
    st.markdown(
        '<p style="text-align:center; color:#444; font-size:12px;">© 2026 <strong style="color:#FFD700;">IT Pro Solutions</strong> - Tous droits réservés</p>',
        unsafe_allow_html=True)
    
