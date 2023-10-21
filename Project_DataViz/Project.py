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

st.header("Welcome to the Data Visualisation Project")

df = pd.read_csv("C:\\Users\\fchan\\OneDrive - Efrei\\M1\\Semestre 7\\Big Data Applications I\\Data Vizualisation\\Streamlit\\dataset.csv", index_col = [0],delimiter=';')
" This project aims to analyze the integration of Masters programs in France. In order to carry out this analysis, we will be using various plotting methods."