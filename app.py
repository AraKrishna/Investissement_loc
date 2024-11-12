import streamlit as st

# Titre de l'application
st.title("Simulation de Rentabilité Locative")

# ---- Création des colonnes ----
col1, col2 = st.columns(2)

# ---- Catégorie : Situation personnelle ----
with col1:
    st.header("Situation personnelle")
    revenu_avant = st.slider("Revenu avant investissement (€)", 1000, 20000, 3350, step=10)
    charge_avant = st.slider("Charges avant investissement (€)", 0, 20000, 3350, step=10)
    mensualite_avant = st.slider("Mensualité avant investissement (€)", 1000, 20000, 3350, step=10)
    pourcentage_revenu_locatif = st.slider("Pourcentage du revenu locatif pris en compte par la banque (%)", 50, 100, 80)

# Calcul du revenu après investissement
revenue_post_investissement = revenu_avant + pourcentage_revenu_locatif

# ---- Catégorie : Bien locatif ----
with col2:
    st.header("Bien locatif")
    prix_achat = st.slider("Prix du bien (€)", 50000, 1000000, 200000, step=5000)
    loyer_mensuel = st.slider("Revenu locatif mensuel (€)", 200, 5000, 800, step=50)
    charges_copropriete = st.slider("Charges de copropriété (mensuel) (€)", 0, 1000, 50, step=10)
    taxe_fonciere = st.slider("Taxe foncière (annuel) (€)", 0, 5000, 500, step=50)
    travaux = st.slider("Travaux (facultatif) (€)", 0, 50000, 0, step=1000)
    interet_annuel = st.slider("Taux d'intérêt du prêt (%)", 0.0, 10.0, 1.5, step=0.1)
    montant_pret = st.slider("Montant du prêt (€)", 0, prix_achat, 100000, step=5000)
    apport = st.slider("Apport personnel (€)", 0, prix_achat, 20000, step=5000)
    duree_pret = st.slider("Durée du prêt (années)", 1, 30, 20)
    taux_assurance = st.slider("Taux d'assurance (%)", 0.0, 1.0, 0.3, step=0.1)

# ---- Calculs de rentabilité ----
# Revenu après investissement
revenu_locatif_annuel = loyer_mensuel * 12
revenu_apres = revenu_avant + (loyer_mensuel * (pourcentage_revenu_locatif / 100))

# Calcul des frais annuels
charges_annuelles = charges_copropriete * 12
frais_annuels_total = charges_annuelles + taxe_fonciere

# Calcul de la mensualité du prêt
# Utilisation de la formule d'annuité pour calculer les mensualités
taux_mensuel = interet_annuel / 100 / 12
mensualite_pret = montant_pret * taux_mensuel / (1 - (1 + taux_mensuel) ** (-duree_pret * 12))

# Calcul de l'assurance sur le prêt
assurance_mensuelle = (montant_pret * (taux_assurance / 100)) / 12
mensualite_totale = mensualite_pret + assurance_mensuelle

# Calcul du coût total du crédit
cout_total_credit = mensualite_totale * duree_pret * 12

# Calculs de rentabilité
rentabilite_brute = (revenu_locatif_annuel / prix_achat) * 100
rentabilite_nette = ((revenu_locatif_annuel - frais_annuels_total) / prix_achat) * 100

# ---- Affichage des résultats ----
st.subheader("Résultats de la Simulation")
st.write(f"Revenu après investissement : {revenu_apres:.2f} €")
st.write(f"Rentabilité brute : {rentabilite_brute:.2f} %")
st.write(f"Rentabilité nette avant impôts : {rentabilite_nette:.2f} %")
st.write(f"Mensualité (prêt + assurance) : {mensualite_totale:.2f} €")
st.write(f"Coût total du crédit : {cout_total_credit:.2f} €")
