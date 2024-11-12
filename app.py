import streamlit as st

# ---- Fonctions utilitaires ----
def calcul_frais_notaires(prix_achat, taux_frais_notaires):
    return (taux_frais_notaires / 100) * prix_achat

def calcul_mensualite_pret(montant_pret, interet_annuel, duree_pret, taux_assurance):
    taux_mensuel = interet_annuel / 100 / 12
    mensualite_pret = montant_pret * taux_mensuel / (1 - (1 + taux_mensuel) ** (-duree_pret * 12))
    assurance_mensuelle = (montant_pret * (taux_assurance / 100)) / 12
    return mensualite_pret + assurance_mensuelle

def calcul_rentabilite_brute(loyer_mensuel, prix_achat):
    revenu_locatif_annuel = loyer_mensuel * 12
    return (revenu_locatif_annuel / prix_achat) * 100

def calcul_rentabilite_nette(loyer_mensuel, frais_annuels_total, cout_total_bien):
    revenu_locatif_annuel = loyer_mensuel * 12
    return ((revenu_locatif_annuel - frais_annuels_total) / cout_total_bien) * 100

# ---- Section Résultats en haut ----
st.title("Simulateur de Rentabilité Locative")
st.subheader("Résultats de la Simulation")

# Données d'entrée (avec valeurs par défaut)
prix_achat = st.session_state.get("prix_achat", 200000)
taux_frais_notaires = st.session_state.get("taux_frais_notaires", 8)
loyer_mensuel = st.session_state.get("loyer_mensuel", 800)
revenu_avant = st.session_state.get("revenu_avant", 3350)
revenu_loc_avant = st.session_state.get("revenu_loc_avant", 0)
mensualite_avant = st.session_state.get("mensualite_avant", 0)
charge_avant = st.session_state.get("charge_avant", 0)

# Calculs
frais_notaires = calcul_frais_notaires(prix_achat, taux_frais_notaires)
cout_total_bien = prix_achat + frais_notaires
frais_annuels_total = st.session_state.get("frais_annuels_total", 0)
mensualite_pret_totale = calcul_mensualite_pret(prix_achat, 3.5, 20, 0.3)
rentabilite_brute = calcul_rentabilite_brute(loyer_mensuel, prix_achat)
rentabilite_nette = calcul_rentabilite_nette(loyer_mensuel, frais_annuels_total, cout_total_bien)

# Affichage des résultats
with st.container():
    col1, col2 = st.columns(2)
    col1.metric("Revenu après investissement (€)", f"{revenu_avant + (loyer_mensuel * 0.8):,.2f}")
    col2.metric("Rentabilité brute (%)", f"{rentabilite_brute:,.2f}")
    
    col3, col4 = st.columns(2)
    col3.metric("Rentabilité nette avant impôts (%)", f"{rentabilite_nette:,.2f}")
    col4.metric("Mensualité totale (€)", f"{mensualite_pret_totale + mensualite_avant:,.2f}")

# ---- Formulaires d'Entrée ----
with st.container():
    st.markdown("### Situation personnelle")
    col1, col2 = st.columns(2)
    with col1:
        revenu_avant = st.number_input("Revenu avant investissement (€)", value=revenu_avant, step=10)
        revenu_loc_avant = st.number_input("Revenu locatif avant investissement (€)", value=revenu_loc_avant, step=10)
        charge_avant = st.number_input("Charges avant investissement (€)", value=charge_avant, step=10)
        mensualite_avant = st.number_input("Mensualité avant investissement (€)", value=mensualite_avant, step=10)
    with col2:
        taux_endettement_actuel = (mensualite_avant / (revenu_avant - charge_avant)) * 100
        col2.metric("Taux d'endettement actuel (%)", f"{taux_endettement_actuel:.2f}")

    st.markdown("### Bien locatif")
    col1, col2 = st.columns(2)
    with col1:
        prix_achat = st.number_input("Prix du bien (€)", value=prix_achat, step=1000)
        taux_frais_notaires = st.slider("Taux des frais de notaires (%)", 1, 15, value=taux_frais_notaires)
        loyer_mensuel = st.number_input("Revenu locatif mensuel (€)", value=loyer_mensuel, step=10)
    with col2:
        apport = st.number_input("Apport personnel (€)", step=5000)
        montant_pret = st.number_input("Montant du prêt (€)", value=prix_achat, step=5000)
        st.metric("Frais de notaires (€)", f"{frais_notaires:,.2f}")

# ---- Calculs finaux et mise à jour session_state ----
st.session_state["frais_annuels_total"] = frais_annuels_total
st.session_state["mensualite_totale"] = mensualite_pret_totale + mensualite_avant
st.session_state["frais_notaires"] = frais_notaires
