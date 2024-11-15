import streamlit as st

# ---- Section Résultats en haut ----
st.title("Simulateur de Rentabilité Locative")
st.subheader("Résultats de la Simulation")


# Conteneur pour afficher les résultats en haut avec une structure plus lisible
with st.container():
    # Calculs préliminaires
    AV_revenu = st.session_state.get("AV_revenu", 3350)  # Valeur par défaut
    loyer_mensuel = st.session_state.get("loyer_mensuel", 800)  # Valeur par défaut
    prix_achat = st.session_state.get("prix_achat", 200000)  # Valeur par défaut
    apport = st.session_state.get("apport", 200000)  # Valeur par défaut
    AV_revenu_locatif = st.session_state.get("AV_revenu_locatif", 0)  # Valeur par défaut
    AV_pourcentage_revenu_locatif = st.session_state.get("AV_pourcentage_revenu_locatif", 80)
    revenu_locatif_annuel = loyer_mensuel * 12

    # Calculs pour le total des revenus et des mensualités
    AV_total_revenu = AV_revenu + (AV_pourcentage_revenu_locatif / 100) * AV_revenu_locatif
    mensualite_pret_totale = st.session_state.get("mensualite_pret_totale", 0)  # Valeur par défaut
    taux_frais_notaires = st.session_state.get("taux_frais_notaires", 8)  # Valeur par défaut : 8%

    # Assurez-vous que "travaux" est défini ou définissez-le ici si il est utilisé plus tard dans calculs
    travaux = st.session_state.get("travaux", 0)
    # Calcul des frais de notaires et coût total du bien
    frais_notaires = (taux_frais_notaires / 100) * prix_achat
    cout_total_bien = prix_achat + frais_notaires + travaux  # Le coût total du bien inclut les frais de notaires

    # Rentabilité brute et nette
    rentabilite_brute = (revenu_locatif_annuel / cout_total_bien) * 100
    rentabilite_nette = ((revenu_locatif_annuel - st.session_state.get("frais_annuels_total", 0)) / cout_total_bien) * 100

    # Calcul du taux d'endettement final
    AV_charges = st.session_state.get("AV_charges", 0)
    AV_mensualite = st.session_state.get("AV_mensualite", 0)
    pourcentage_revenu_locatif = st.session_state.get("pourcentage_revenu_locatif", 80)
    taux_endettement_final = (
        (mensualite_pret_totale + AV_mensualite) /
        (AV_charges + AV_revenu + AV_revenu_locatif * (AV_pourcentage_revenu_locatif / 100) + loyer_mensuel * pourcentage_revenu_locatif / 100)
    ) * 100

    # Calcul du cashflow mensuel
    frais_annuels_total = st.session_state.get("frais_annuels_total", 0)
    cashflow_mensuel = loyer_mensuel - (frais_annuels_total / 12) - mensualite_pret_totale
    frais_mensuels = frais_annuels_total / 12

    # Organisation des résultats sur deux lignes
    col1, col2 = st.columns([1, 1])  # Première ligne
    col1.metric("Revenu après investissement (€)", f"{AV_revenu + AV_revenu_locatif + (loyer_mensuel)-frais_mensuels :,.2f}".replace(',', ' '))
    col2.metric("Rentabilité brute (%)", f"{rentabilite_brute:,.2f}".replace(',', ' '))
    st.caption("_La rentabilité brute est le pourcentage du revenu locatif annuel par rapport au coût total du bien (prix d'achat + frais de notaires)._")
    st.caption("_La rentabilité nette est la rentabilité après déduction des charges et taxes, avant impôts._")
    
    col3, col4 = st.columns([1, 1])  # Deuxième ligne
    col3.metric("Rentabilité nette avant impôts (%)", f"{rentabilite_nette:,.2f}".replace(',', ' '))
    
    col4.metric("Mensualité totale (€)", f"{mensualite_pret_totale + AV_mensualite:,.2f}".replace(',', ' '))
    
    st.subheader(f"Taux d'endettement final (%) : {taux_endettement_final:,.2f}")
    st.write("---")  # Ligne de séparation pour mieux structurer la page
    
    col5, col6 = st.columns([1, 1])  # Troisième ligne (pour cashflow et mensualités du nouveau prêt)
    col5.metric("Cashflow mensuel (€) - nouveau bien", f"{cashflow_mensuel:,.2f}".replace(',', ' '))
    st.caption("_Le cashflow mensuel est le montant restant chaque mois après le paiement des charges et des mensualités._")
    col6.metric("Mensualité (prêt + assurance) - nouveau prêt (€)", f"{mensualite_pret_totale:,.2f}".replace(',', ' '))
    st.write("---")  # Ligne de séparation pour mieux structurer la page


# ---- Formulaire d'Entrées : Situation personnelle ---------------------------
with st.container():
    st.markdown("### Situation personnelle")
    col1, col2 = st.columns(2)
    with col1:
        AV_revenu = st.number_input("Revenu avant investissement (€)", min_value=1000, max_value=20000, value=3350, step=10, key="AV_revenu")
        AV_revenu_locatif = st.number_input("Revenu locatif avant investissement (€)", min_value=0, max_value=20000, value=0, step=10, key="AV_revenu_locatif")
        AV_pourcentage_revenu_locatif = st.slider("Pourcentage du revenu locatif pris en compte par la banque (%) - Avant investissement", 50, 100, 80)
        AV_charges = st.number_input("Charges avant investissement (€)", min_value=0, max_value=20000, value=0, step=10, key="AV_charges")
        AV_mensualite = st.number_input("Mensualité avant investissement (€)", min_value=0, max_value=20000, value=0, step=10, key="AV_mensualite")

    with col2:
        AV_total_revenu = AV_revenu + (AV_pourcentage_revenu_locatif / 100) * AV_revenu_locatif
        col2.metric("Taux d'endettement actuel (%)", f"{AV_mensualite / (AV_total_revenu - AV_charges) * 100:,.2f}".replace(',', ' '))
st.write("---")  # Ligne de séparation pour mieux structurer la page

# ---- Formulaire d'Entrées : Bien locatif ------------------------
with st.container():
    st.markdown("### Bien locatif")
    col1, col2 = st.columns(2)
    with col1:
        prix_achat = st.number_input("Prix du bien (€) - Frais d'agence compris", min_value=0, max_value=4000000, value=100000, step=1000, key="prix_achat")
        travaux = st.number_input("Travaux (facultatif) (€)", min_value=0, max_value=200000, value=0, step=1000)
        taux_frais_notaires = st.slider("Taux des frais de notaires (%)", 1, 15, 8, key="taux_frais_notaires")
        loyer_mensuel = st.number_input("Revenu locatif mensuel (€)", min_value=0, max_value=5000, value=500, step=10, key="loyer_mensuel")
        charges_copropriete = st.number_input("Charges de copropriété (mensuel) (€)", min_value=0, max_value=1000, value=200, step=5)
        taxe_fonciere = st.number_input("Taxe foncière (annuel) (€)", min_value=0, max_value=5000, value=200, step=10)

    with col2:
        apport = st.number_input("Apport personnel (€)", min_value=0, max_value=4000000, value=0, step=5000)
        montant_pret = st.number_input("Montant du prêt (€)", min_value=0, max_value=4000000, value=prix_achat, step=1000)
        interet_annuel = st.number_input("Taux d'intérêt du prêt (%)", min_value=0.0, max_value=10.0, value=3.5, step=0.1)
        taux_assurance = st.number_input("Taux d'assurance (%)", min_value=0.0, max_value=4.0, value=0.3, step=0.1)
        duree_pret = st.slider("Durée du prêt (années)", 1, 30, 20)
        pourcentage_revenu_locatif = st.slider("Pourcentage du revenu locatif pris en compte par la banque (%)", 50, 100, 80)

    frais_notaires = (taux_frais_notaires / 100) * prix_achat
    st.metric("Frais de notaires (€)", f"{frais_notaires:,.2f}".replace(',', ' '))
st.write("---")  # Ligne de séparation pour mieux structurer la page

# ---- Calculs et mise à jour des valeurs dans session_state ----
frais_annuels_total = (charges_copropriete * 12) + taxe_fonciere
cout_total_bien = prix_achat + frais_notaires + travaux
taux_mensuel = interet_annuel / 100 / 12
mensualite_pret = montant_pret * taux_mensuel / (1 - (1 + taux_mensuel) ** (-duree_pret * 12))
mensualite_assurance = (montant_pret * taux_assurance / 100) / 12
mensualite_pret_totale = mensualite_pret + mensualite_assurance

st.session_state.update({
    "AV_total_revenu": AV_total_revenu,
    "mensualite_pret_totale": mensualite_pret_totale,
    "frais_annuels_total": frais_annuels_total,
})
