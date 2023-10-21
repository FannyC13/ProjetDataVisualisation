import streamlit as st
import streamlit as st
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import streamlit as st


st.header("Plotting Data")

df = pd.read_csv('data_cleaned_insertion_pro.csv')

st.dataframe(df)

st.sidebar.title("Menu de Navigation")
choix = st.sidebar.radio("Sélectionnez une option", ["Nombre de Réponse", "Analyse Type Emploi"])


if choix == "Nombre de Réponse":

#-------------------------------------------------------------Réponses par académies par années------------------------------------------------------------------#
    count_academie = df["academie"].value_counts()
    
    st.write("Nombre d'occurences par académies", count_academie)

    st.subheader("Plot Du Nombre de réponses par académies")

    annees = df["annee"].unique()
    selected_annees = st.multiselect("Sélectionnez les années (academie)", annees,annees)

    df_reponses_par_academie_par_annee = df[df["annee"].isin(selected_annees)].groupby("academie")["nombre_de_reponses"].sum().reset_index()

    fig = px.bar(df_reponses_par_academie_par_annee, x="academie", y="nombre_de_reponses", title="Nombre de Réponses par Académie")
    st.plotly_chart(fig)

#-------------------------------------------------------------Réponses par domaine par années------------------------------------------------------------------#

    st.subheader("Plot Du Nombre de réponses par domaine")

    annees = df["annee"].unique()
    selected_annees = st.multiselect("Sélectionnez les années (domaine)", annees,annees)

    df_reponses_par_domaine_par_annee = df[df["annee"].isin(selected_annees)].groupby("domaine")["nombre_de_reponses"].sum().reset_index()

    fig = px.bar(df_reponses_par_domaine_par_annee, x="domaine", y="nombre_de_reponses", title="Nombre de Réponses par domaine")
    st.plotly_chart(fig)


elif choix == "Analyse Type Emploi":

    st.subheader("Analyse Emploi")

    Bar1, Line, Bar2 = st.tabs(["Bar Plot", "Line Chart", "Bar Empilées"])

    st.subheader("Plot Evolution Du Nombre de cadre par discipline")

    annees = df["annee"].unique()
    selected_annees = st.multiselect("Sélectionnez les années (cadres)", annees,annees)
    
    df_cadres_par_discipline_par_annee = df[df["annee"].isin(selected_annees)].groupby(["annee", "discipline"])["emplois_cadre"].sum().reset_index()
    #df_cadres_par_discipline_par_annee = df[df["annee"].isin(selected_annees)].groupby("discipline")["emplois_cadre"].sum().reset_index()
    plot_choice = st.radio("Select a Plot", ["Bar Chart 1", "Line Chart", "Bar Chart 2"])

    if plot_choice == "Bar Chart 1":
        fig = px.bar(df_cadres_par_discipline_par_annee, x="discipline", y="emplois_cadre", title="Nombre d'emplois cadre par discipline")
        st.plotly_chart(fig)

    elif plot_choice == "Line Chart":
        fig = px.line(df_cadres_par_discipline_par_annee, x="annee", y="emplois_cadre", color="discipline", title="Nombre d'emplois cadre par discipline")
        st.plotly_chart(fig)

    elif plot_choice == "Bar Chart 2":
        fig = px.bar(df_cadres_par_discipline_par_annee, x="annee", y="emplois_cadre", color="discipline", title="Nombre d'emplois cadre par discipline")
        st.plotly_chart(fig)

