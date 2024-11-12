import streamlit as st

# ---- Section de Titre ----
st.title("Simulateur de Rentabilité Locative")
st.markdown("## Résultats de la Simulation")
st.write("---")  # Ligne de séparation pour une meilleure lisibilité

# ---- Section Résultats ----
with st.container():
    st.markdown("### Résultats Financiers")
    col1, col2 = st.columns(2)  # Première ligne
    with col1:
        col1.metric("Revenu après investissement (€)", f"{Total_revenu_avant + (loyer_mensuel * 0.8):,.2f}".replace(',', ' '))
    with col2:
        col2.metric("Rentabilité brute (%)", f"{rentabilite_brute:,.2f}".replace(',', ' '))

    col3, col4 = st.columns(2)  # Deuxième ligne
    with col3:
        col3.metric("Rentabilité nette avant impôts (%)", f"{rentabilite_nette:,.2f}".replace(',', ' '))
    with col4:
        col4.metric("Mensualité totale (€)", f"{mensualite_totale:,.2f}".replace(',', ' '))

    st.subheader(f"Taux d'endettement final (%) : {taux_endettement_final:,.2f}")
    st.write("---")  # Ligne de séparation pour mieux structurer la page

    # Troisième ligne avec cashflow et mensualité du nouveau prêt
    col5, col6 = st.columns(2)
    with col5:
        col5.metric("Cashflow mensuel (€) - nouveau bien", f"{cashflow_mensuel:,.2f}".replace(',', ' '))
    with col6:
        col6.metric("Mensualité (prêt + assurance)  - nouveau prêt (€)", f"{mensualite_totale:,.2f}".replace(',', ' '))

    st.write("---")  # Ligne de séparation pour mieux structurer la page

# ---- Formulaire d'Entrées : Situation personnelle ----
with st.expander("Situation personnelle", expanded=True):
    st.markdown("### Vos informations personnelles")
    col1, col2 = st.columns(2)
    with col1:
        revenu_avant = st.number_input("Revenu avant investissement (€)", min_value=1000, max_value=20000, value=3350, step=10, key="revenu_avant")
        revenu_loc_avant = st.number_input("Revenu locatif avant investissement (€)", min_value=0, max_value=20000, value=0, step=10, key="revenu_loc_avant")
        pourcentage_revenu_locatif_avant = st.slider("Pourcentage du revenu locatif pris en compte par la banque (%) - Avant investissement", 50, 100, 80)
        charge_avant = st.number_input("Charges avant investissement (€)", min_value=0, max_value=20000, value=0, step=10)
        mensualite_avant = st.number_input("Mensualité avant investissement (€)", min_value=0, max_value=20000, value=0, step=10)
    
    with col2:
        col2.metric("Taux d'endettement actuel (%)", f"{mensualite_avant/(revenu_avant - charge_avant)*100:,.2f}".replace(',', ' '))

# ---- Formulaire d'Entrées : Bien locatif ----
with st.expander("Détails du bien locatif", expanded=True):
    st.markdown("### Informations sur le bien locatif")
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
        montant_pret = st.number_input("Montant du prêt (€)", min_value=0, max_value=4000000, value=prix_achat, step=5000)
        interet_annuel = st.number_input("Taux d'intérêt du prêt (%)", min_value=0.0, max_value=10.0, value=3.5, step=0.1)
        taux_assurance = st.number_input("Taux d'assurance (%)", min_value=0.0, max_value=4.0, value=0.3, step=0.1)
        duree_pret = st.slider("Durée du prêt (années)", 1, 30, 20)
        pourcentage_revenu_locatif = st.slider("Pourcentage du revenu locatif pris en compte par la banque (%)", 50, 100, 80)
        
    # Affichage des frais de notaires calculés dans une métrique
    frais_notaires = (taux_frais_notaires / 100) * prix_achat  # Calcul des frais de notaires
    st.metric("Frais de notaires (€)", f"{frais_notaires:,.2f}".replace(',', ' '))

# ---- Calculs et mise à jour des valeurs dans session_state ----
frais_annuels_total = (charges_copropriete * 12) + taxe_fonciere
frais_notaires = (taux_frais_notaires / 100) * prix_achat  # Calcul des frais de notaires avec le taux personnalisé
cout_total_bien = prix_achat + frais_notaires  # Le coût total du bien inclut maintenant les frais de notaires
taux_mensuel = interet_annuel / 100 / 12
mensualite_pret = montant_pret * taux_mensuel / (1 - (1 + taux_mensuel) ** (-duree_pret * 12))
assurance_mensuelle = (montant_pret * (taux_assurance / 100)) / 12
mensualite_pret_totale = mensualite_pret + assurance_mensuelle
cashflow_mensuel = loyer_mensuel - frais_annuels_total / 12

cout_total_credit = mensualite_pret_totale * duree_pret * 12

# Mise à jour des résultats calculés dans session_state pour les afficher en haut
st.session_state["frais_annuels_total"] = frais_annuels_total
st.session_state["mensualite_totale"] = mensualite_pret_totale + mensualite_avant
st.session_state["cout_total_credit"] = cout_total_credit
st.session_state["frais_notaires"] = frais_notaires  # Mise à jour des frais de notaires

# ---- Section de Résultats Finaux ----
st.write("---")
st.markdown("### Récapitulatif des Calculs")

# Affichage des informations clés sous forme de tableau ou liste
st.write(f"**Coût total du bien** : {cout_total_bien:,.2f} €")
st.write(f"**Coût total du crédit** : {cout_total_credit:,.2f} €")
st.write(f"**Cashflow mensuel** : {cashflow_mensuel:,.2f} €")
st.write(f"**Mensualité totale du prêt (prêt + assurance)** : {mensualite_pret_totale:,.2f} €")
st.write(f"**Rentabilité brute** : {rentabilite_brute:,.2f} %")
st.write(f"**Rentabilité nette avant impôts** : {rentabilite_nette:,.2f} %")
st.write(f"**Taux d'endettement final** : {taux_endettement_final:,.2f} %")

