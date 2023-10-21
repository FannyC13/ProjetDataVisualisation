import streamlit as st
import streamlit as st
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import streamlit as st
import json
import folium
from streamlit_folium import folium_static


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

    #-------------------------------------------------------------Evolution Du Nombre de cadre par discipline------------------------------------------------------------------#

    Bar1, Line, Bar2 = st.tabs(["Bar Plot", "Line Chart", "Bar Empilées"])

    st.subheader("Plot Evolution Du Nombre de cadre par discipline")

    annees = df["annee"].unique()
    selected_annees = st.multiselect("Sélectionnez les années (cadres)", annees,annees)
    
    df_cadres_par_discipline_par_annee = df[df["annee"].isin(selected_annees)].groupby(["annee", "discipline"])["emplois_cadre"].sum().reset_index()
    
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

    #------------------------------------------------------------- Taux d'insertion par discipline------------------------------------------------------------------#

    st.subheader("Plot Du Taux d'insertion par discipline")

    selected_annees = st.multiselect("Sélectionnez les années", annees,annees, key="taux_insertion_par_discipline")

    df_insertion_par_disicpline_par_annee = df[df["annee"].isin(selected_annees)].groupby("discipline")["taux_dinsertion"].mean().reset_index()

    fig = px.bar(df_insertion_par_disicpline_par_annee, x="discipline", y="taux_dinsertion", title="Taux d'insertion par discipline")
    
    for i in range(len(df_insertion_par_disicpline_par_annee)):
        discipline = df_insertion_par_disicpline_par_annee.loc[i, "discipline"]
        taux_insertion = df_insertion_par_disicpline_par_annee.loc[i, "taux_dinsertion"]
        taux_insertion_percentage = f"{taux_insertion:.2f}%" 
        fig.add_annotation(
            x=discipline,
            y=taux_insertion,
            text=f"{taux_insertion_percentage}", 
            showarrow=False,
            font=dict(size=9),
            yshift=12
        )

    st.plotly_chart(fig)

    #-------------------------------------------------------------Taux d'insertion par academie------------------------------------------------------------------#

    st.subheader("Plot Du Taux d'insertion par academie")
    
    selected_annees = st.multiselect("Sélectionnez les années (academie)", annees,annees, key="taux_insertion_par_academie")
    df_insertion_par_academie_par_annee = df[df["annee"].isin(selected_annees)].groupby("academie")["taux_dinsertion"].mean().reset_index()
    
    plot_choice_2 = st.radio("Select a Plot", ["Map", "Bar Chart"])

    if plot_choice_2 == "Bar Chart":
        fig = px.bar(df_insertion_par_academie_par_annee, x="academie", y="taux_dinsertion", title="Taux d'insertion par academie")

        for i in range(len(df_insertion_par_academie_par_annee)):
            academie = df_insertion_par_academie_par_annee.loc[i, "academie"]
            taux_insertion = df_insertion_par_academie_par_annee.loc[i, "taux_dinsertion"]
            taux_insertion_percentage = f"{taux_insertion:.1f}%" 
            fig.add_annotation(
                x=academie,
                y=taux_insertion,
                text=f"{taux_insertion_percentage} ", 
                showarrow=False,
                font=dict(size=9),
                yshift=13
            )

        st.plotly_chart(fig)
   
    if plot_choice_2 == "Map":
    
        with open('academie.geojson') as f:
            geojson_data = json.load(f)

        m = folium.Map(location=[48.8566, 2.3522], zoom_start=5) #France

        for feature in geojson_data['features']:
            academie = feature['properties']['name']
            taux_dinsertion = df_insertion_par_academie_par_annee[df_insertion_par_academie_par_annee['academie'] == academie]['taux_dinsertion'].mean()
            feature['properties']['taux_dinsertion'] = taux_dinsertion

            latitude, longitude = feature['properties']['geo_point_2d']
            tooltip = f'{academie}<br>Taux d\'Insertion : {taux_dinsertion:.2f}%'
            folium.Marker(
                location=[latitude, longitude],
                tooltip=tooltip,
                icon=folium.DivIcon(
                    icon_size=(20, 20), 
                    icon_anchor=(10, 10),
                    html=f'<i class="fa fa-map-marker fa-2x" style="color: #61677A;"></i>' 
                )
            ).add_to(m)


        folium.Choropleth(
            geo_data=geojson_data,
            data=df_insertion_par_academie_par_annee,
            columns=['academie', 'taux_dinsertion'],
            key_on='feature.properties.name',
            fill_color='Pastel1',
            fill_opacity=0.5,
            line_opacity=0.2,
            legend_name='Taux d\'Insertion (%)',
            threshold_scale=[82,84, 86, 88, 90, 92,94,96]
        ).add_to(m)

        st.title('Carte des Taux d\'Insertions par Académie')
        folium_static(m)