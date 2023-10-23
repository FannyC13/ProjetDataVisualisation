import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from ydata_profiling import ProfileReport

st.set_page_config(layout="wide")

st.header("Exploratory Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv("fr-esr-insertion_professionnelle-master.csv", delimiter=';')
    return df

@st.cache_data  
def clean_and_preprocess_data(df):

    df = df.replace('ns', np.nan)
    df = df.replace('nd', np.nan)
    df = df.drop(['remarque', 'etablissementactuel', 'code_de_l_academie', 'code_de_la_discipline', 'cle_etab', 'cle_disc'], axis=1)

    for col in ['taux_dinsertion', 'emplois_cadre_ou_professions_intermediaires', 'emplois_stables', 'emplois_a_temps_plein', 'salaire_net_median_des_emplois_a_temps_plein', 'salaire_brut_annuel_estime', 'de_diplomes_boursiers', 'taux_de_chomage_regional', 'salaire_net_mensuel_median_regional', 'emplois_cadre', 'emplois_exterieurs_a_la_region_de_luniversite', 'femmes', 'salaire_net_mensuel_regional_1er_quartile', 'salaire_net_mensuel_regional_3eme_quartile']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(axis=0, thresh=df.shape[1] - 4, inplace=True)

    df = df.loc[(df['annee'] != 2010) & (df['annee'] != 2011)]

    return df

df = load_data()

"Ces informations sont basées sur les données collectées dans le cadre de l'opération nationale de collecte de données sur l’insertion professionnelle des diplômés de Master"

tab1, tab2, tab3 = st.tabs(["Informations", "Data Profiling", "Data Cleaning"])

with tab1:
    st.dataframe(df)
    "Colonnes :"
    
    "- nombre_de_reponses : Nombre de réponses"
    "- taux_de_reponse : Taux de réponse"
    "- poids_de_la_discipline : Poids de la discipline"
    "- emplois_cadre_ou_professions_intermediaires : Part des emplois de niveau cadre ou profession intermédiaire"
    "- emplois_stables : Part des emplois stables"
    "- emplois_a_temps_plein : Part des emplois à temps plein"
    "- salaire_net_median_des_emplois_a_temps_plein : Salaire net mensuel médian des emplois à temps plein"
    "- salaire_brut_annuel_estime : Salaire brut annuel médian estimé de_diplomes_boursiers : Part des diplômés boursiers dans l'établissement"
    "- taux_de_chomage_regional : Taux de chômage régional (INSEE : 4ème trimestre N+2)"
    "- salaire_net_mensuel_median_regional : Salaire mensuel net médian des jeunes de 25 à 29 ans employés à temps plein dans les catégories cadre et professions intermédiaires (INSEE : DADS N)"
    "- taux_dinsertion : Taux d'insertion"
    "- emplois_cadre : Part des emplois de niveau cadre (Dans certains secteurs d'activité, les emplois correspondants au diplôme ne sont pas tous de niveau cadre. L'accès au niveau cadre peut nécessiter une expérience professionnelle préalable.)"
    "- emplois_exterieurs_a_la_region_de_luniversite Part des emplois situés en dehors de la région de l'établissement (y compris à l'étranger)"
    "- femmes : Part des femmes"
    

with tab2:
    st.header("Test Profile")
    report_generated = False
    report = ProfileReport(df, title="Profiling Report", minimal=True)

    report_generated = False
    report_downloaded = False

    report = ProfileReport(df, title="Profiling Report", minimal=True)
    import time

    if not report_generated:
        if st.button("Generate HTML Report", key="generate_report_button"):
            st.info("Generating report...")
            st_profile_report(report)
            report_generated = True

with tab3:
    st.header("Data Cleaning")
    cleaned_df = clean_and_preprocess_data(df)

    st.dataframe(df)

    "Beaucoup de colonnes ont des observations où il est marqué 'ns' (non significatives : moins de 30 répondants) ou 'nd' (non disponibles). L'idée est de nettoyer un maximum de ces valeurs."
    st.code('''
    df = df.replace('ns', np.nan)
    df = df.replace('nd', npnan)
    ''', language='python')

    "On supprime les colonnes contenant trop de valeurs NaN, car le nombre d'observations n'est pas suffisant pour faire des analyses dessus."
    st.code('''
    print((df.isna().mean() * 100).sort_values(ascending=False))
    ''', language='python')

    st.dataframe((df.isna().mean() * 100).sort_values(ascending=False))

    
    "Tous les codes et clés sont redondants. On les enlève aussi."

    st.code(
        '''
        df = df.drop('remarque', axis=1)
        df = df.drop('etablissementactuel', axis=1)
        df = df.drop('code_de_l_academie', axis=1)
        df = df.drop('code_de_la_discipline', axis=1)
        df = df.drop('cle_etab', axis=1)
        df = df.drop('cle_disc', axis=1)''', language = 'python')

    "Beaucoup de colonnes ne sont pas encodées avec une valeur numérique, ce qui nous empêche de faire les visualisations. Changeons cela."

    st.write(df.dtypes)

    st.code('''
        for col in ['taux_dinsertion', 'emplois_cadre_ou_professions_intermediaires', 'emplois_stables', 'emplois_a_temps_plein', 'salaire_net_median_des_emplois_a_temps_plein', 'salaire_brut_annuel_estime', 'de_diplomes_boursiers', 'taux_de_chomage_regional', 'salaire_net_mensuel_median_regional', 'emplois_cadre', 'emplois_exterieurs_a_la_region_de_luniversite', 'femmes', 'salaire_net_mensuel_regional_1er_quartile', 'salaire_net_mensuel_regional_3eme_quartile']:
        df[col] = pd.to_numeric(df[col],errors='coerce')''')

    st.write(cleaned_df.dtypes)

    "On supprime les observations qui contiennent trop peu de valeurs. Si une observation contient 5 NaN ou +, on la supprime."

   
    lignes_plus_de_5_nan = df[df.isna().sum(axis=1) > 5]
    colonnes_avec_nan = lignes_plus_de_5_nan.columns[lignes_plus_de_5_nan.isna().any()]
    df_avec_nan = lignes_plus_de_5_nan[colonnes_avec_nan]

    st.write("DataFrame avec les lignes contenant au moins 5 NaN:")
    st.write(df_avec_nan)

    st.code('''
            df.dropna(axis=0, thresh=df.shape[1] - 4, inplace=True) 
            df.shape''')
    
    "On aimerait faire des visualisations par années, mais nous avons peur d'avoir trop peu d'observations dans certaines années. Regardons la part de chaque année dans le dataframe."
    
    fig = px.histogram(df["annee"], nbins=19, title="Histogram of 'annee'")
    st.plotly_chart(fig)

    "Il y a environ le même nombre d'observations sur toutes les années à part 2011. Enlevons cette année."
    st.code('''
    df = df.loc[(df['annee'] != 2010) & (df['annee'] != 2011)]
    df.shape
    ''', language='python')

    st.write(cleaned_df.shape)

    "Regardons une dernière fois la répartition des NaN par colonne pour voir si notre dataset fait du sens."

    st.write((cleaned_df.isna().mean() * 100).sort_values(ascending=False))

    "C'est magnifique. Regardons une dernière fois le dataframe avant de l'exporter."
    st.dataframe(cleaned_df)
    st.code("cleaned_df.to_csv('data_cleaned_insertion_pro.csv')")

    cleaned_df.to_csv('data_cleaned_insertion_pro.csv')