import streamlit as st

# ---- Section Résultats en haut ----
st.title("Simulation de Rentabilité Locative")
st.subheader("Résultats de la Simulation")

# Conteneur pour afficher les résultats en haut avec une structure plus lisible
with st.container():
    # Calculs préliminaires
    revenu_avant = st.session_state.get("revenu_avant", 3350)  # Valeur par défaut
    loyer_mensuel = st.session_state.get("loyer_mensuel", 800)  # Valeur par défaut
    prix_achat = st.session_state.get("prix_achat", 200000)  # Valeur par défaut

    revenu_locatif_annuel = loyer_mensuel * 12
    rentabilite_brute = (revenu_locatif_annuel / prix_achat) * 100
    rentabilite_nette = ((revenu_locatif_annuel - st.session_state.get("frais_annuels_total", 0)) / prix_achat) * 100
    mensualite_totale = st.session_state.get("mensualite_totale", 0)
    cout_total_credit = st.session_state.get("cout_total_credit", 0)

    # Organisation des résultats principaux sur une ligne, avec des colonnes larges pour les lire d'un coup d'œil
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])  # Ajustement des largeurs pour plus de lisibilité
    col1.metric("Revenu après investissement (€)", f"{revenu_avant + (loyer_mensuel * 0.8):,.2f}".replace(',', ' '))
    col2.metric("Rentabilité brute (%)", f"{rentabilite_brute:,.2f}".replace(',', ' '))
    col3.metric("Rentabilité nette avant impôts (%)", f"{rentabilite_nette:,.2f}".replace(',', ' '))
    col4.metric("Mensualité (prêt + assurance) (€)", f"{mensualite_totale:,.2f}".replace(',', ' '))

    st.write("---")  # Ligne de séparation pour mieux structurer la page

# ---- Formulaire d'Entrées : Situation personnelle ----
with st.container():
    st.markdown("### Situation personnelle")
    col1, col2 = st.columns(2)
    
    with col1:
        revenu_avant = st.number_input("Revenu avant investissement (€)", min_value=1000, max_value=20000, value=3350, step=10, key="revenu_avant")
        charge_avant = st.number_input("Charges avant investissement (€)", min_value=0, max_value=20000, value=0, step=10)
        mensualite_avant = st.number_input("Mensualité avant investissement (€)", min_value=0, max_value=20000, value=0, step=10)
    
    with col2:
        col2.metric("Taux d'endettement actuel (%)", f"{mensualite_avant/(revenu_avant - charge_avant)*100:,.2f}".replace(',', ' '))
        

# ---- Formulaire d'Entrées : Bien locatif ----
with st.container():
    st.markdown("### Bien locatif")
    col1, col2 = st.columns(2)

    with col1:
        prix_achat = st.number_input("Prix du bien (€) - Frais d'agence compris", min_value=0, max_value=4000000, value=100000, step=1000, key="prix_achat")
        frais_de_notaires = st.number_input("Frais de notaires (€)", min_value=0.0, max_value=4000000, value=0.08*prix_achat, step=100)
        loyer_mensuel = st.number_input("Revenu locatif mensuel (€)", min_value=0, max_value=5000, value=500, step=10, key="loyer_mensuel")
        charges_copropriete = st.number_input("Charges de copropriété (mensuel) (€)", min_value=0, max_value=1000, value=200, step=5)
        taxe_fonciere = st.number_input("Taxe foncière (annuel) (€)", min_value=0, max_value=5000, value=200, step=10)
        pourcentage_revenu_locatif = st.slider("Pourcentage du revenu locatif pris en compte par la banque (%)", 50, 100, 80)
        duree_pret = st.slider("Durée du prêt (années)", 1, 30, 20)
        taux_assurance = st.number_input("Taux d'assurance (%)", min_value=0.0, max_value=4.0, value=0.3, step=0.1)
    

    with col2:
        travaux = st.number_input("Travaux (facultatif) (€)", min_value=0, max_value=200000, value=0, step=1000)
        interet_annuel = st.number_input("Taux d'intérêt du prêt (%)", min_value=0.0, max_value=10.0, value=3.5, step=0.1)
        montant_pret = st.number_input("Montant du prêt (€)", min_value=0, max_value=4000000, value=prix_achat, step=5000)
        apport = st.number_input("Apport personnel (€)", min_value=0, max_value=4000000, value=0.08*prix_achat, step=5000)

    

# ---- Calculs et mise à jour des valeurs dans session_state ----
# Calcul des frais annuels et mensualités
frais_annuels_total = (charges_copropriete * 12) + taxe_fonciere
taux_mensuel = interet_annuel / 100 / 12
mensualite_pret = montant_pret * taux_mensuel / (1 - (1 + taux_mensuel) ** (-duree_pret * 12))
assurance_mensuelle = (montant_pret * (taux_assurance / 100)) / 12
mensualite_totale = mensualite_pret + assurance_mensuelle
cout_total_credit = mensualite_totale * duree_pret * 12

# Mise à jour des résultats calculés dans session_state pour les afficher en haut
st.session_state["frais_annuels_total"] = frais_annuels_total
st.session_state["mensualite_totale"] = mensualite_totale
st.session_state["cout_total_credit"] = cout_total_credit
