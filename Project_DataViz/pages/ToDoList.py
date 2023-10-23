import streamlit as st
st.set_option("deprecation.showfileUploaderEncoding", False)

if 'checkbox_state' not in st.session_state:
    st.session_state.checkbox_state = {
        "Taux de chômage par discipline": False,
        "Cartes avec d'autres variables": False,
        "Taux de femmes par filière": False,
        "Corrélations entre le genre et d'autres variables": False,
        "Salaires par filière": False,
        "Salaires en fonction de la discipline": False,
        "Histogramme des salaires en sortie d'études": False,
        "Bar Chart Empilé": False,
        "Analyses": False,
    }

@st.cache(allow_output_mutation=True)
def update_checkbox_state():
    checkbox_state = st.session_state.checkbox_state
    return checkbox_state

checkbox_state = update_checkbox_state()

# Page 1 : INSERTION POST DIPLOME
st.title("INSERTION POST DIPLOME")

checkbox_state["Taux de chômage par discipline"] = st.checkbox(
    "Taux de chômage par discipline : 100 - taux d'insersion (mais quid des doctorants ?)", checkbox_state["Taux de chômage par discipline"]
)
checkbox_taux_chomage_discipline = checkbox_state["Taux de chômage par discipline"]

checkbox_state["Cartes avec d'autres variables"] = st.checkbox(
    "Rajouter des cartes avec d'autres variables que le taux d'insertion : taux de cadres, taux d'emplois stables, etc", checkbox_state["Cartes avec d'autres variables"]
)
checkbox_cartes_variables = checkbox_state["Cartes avec d'autres variables"]

checkbox_state["Bar Chart Empilé"] = st.checkbox(
    "Bar chart empilé avec : nombre de cadres, nombre de chomeurs (100 - emploi stable), nombre de personnes ni cadres ni chomeurs (100 - cadres - chomeurs)", checkbox_state["Bar Chart Empilé"]
)
checkbox_bar_chart_empile = checkbox_state["Bar Chart Empilé"]


checkbox_state["Analyses"] = st.checkbox(
    "Ajouter les Analyses", checkbox_state["Analyses"]
)
checkbox_bar_chart_empile = checkbox_state["Analyses"]

# Page 2 : IMPACT DU GENRE
st.title("IMPACT DU GENRE")
checkbox_state["Taux de femmes par filière"] = st.checkbox(
    "Taux de femmes par filière", checkbox_state["Taux de femmes par filière"]
)
checkbox_taux_femmes_filiere = checkbox_state["Taux de femmes par filière"]

checkbox_state["Corrélations entre le genre et d'autres variables"] = st.checkbox(
    "Corrélations entre le genre et d'autres variables", checkbox_state["Corrélations entre le genre et d'autres variables"]
)
checkbox_correlations = checkbox_state["Corrélations entre le genre et d'autres variables"]

# Page 3 : ÉLÉMENTS IMPACTANT LE SALAIRE
st.title("ÉLÉMENTS IMPACTANT LE SALAIRE")
checkbox_state["Salaires par filière"] = st.checkbox(
    "Salaires par filière", checkbox_state["Salaires par filière"]
)
checkbox_salaires_filiere = checkbox_state["Salaires par filière"]

checkbox_state["Salaires en fonction de la discipline"] = st.checkbox(
    "Salaires en fonction de la discipline", checkbox_state["Salaires en fonction de la discipline"]
)
checkbox_salaires_discipline = checkbox_state["Salaires en fonction de la discipline"]

checkbox_state["Histogramme des salaires en sortie d'études"] = st.checkbox(
    "Histogramme des salaires en sortie d'études", checkbox_state["Histogramme des salaires en sortie d'études"]
)
checkbox_histogramme = checkbox_state["Histogramme des salaires en sortie d'études"]
