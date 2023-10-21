import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import streamlit as st
from streamlit_pandas_profiling import st_profile_report
from ydata_profiling import ProfileReport
import base64

st.header("Bienvenue sur notre projet de visualisation de données :smile:")

df = pd.read_csv("C:\\Users\\fchan\\OneDrive - Efrei\\M1\\Semestre 7\\Big Data Applications I\\Data Vizualisation\\Streamlit\\dataset.csv", index_col = [0],delimiter=';')
"Ce projet vise à analyser l'intégration des masters en France. Pour mener à bien cette analyse, nous utiliserons différentes méthodes de représentation graphique"

"Cette page est la page principale du projet, vous trouverez dans 'Exploratory Analysis' toutes les informations concernant le jeu de données ainsi que les détails du profiling et du data cleaning"
"La page 'Plotting' contient les différents plot qui nous permettront d'effectuer une analyse approfondie de l'ensemble des données. Cette page est divisée en différentes sections pour une meilleure vue d'ensemble de l'analyse"