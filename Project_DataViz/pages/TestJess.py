import pandas as pd
import streamlit as st
url = 'https://static.data.gouv.fr/resources/activite-chirurgicale-en-cancerologie-par-localisation-tumorale/20180220-154105/Activite_chirurgicale_en_cancerologie_par_localisation_tumorale.csv'
data = pd.read_csv(url, header=0, encoding='ISO-8859-1',delimiter=';', skiprows=1)

st.dataframe(data)