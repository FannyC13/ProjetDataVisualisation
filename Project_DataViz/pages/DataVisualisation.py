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
import seaborn as sns
from functools import wraps
import time

st.set_page_config(layout="wide")

#Création d'un cache pour load la data
@st.cache_data
def load_data():
    df = pd.read_csv('data_cleaned_insertion_pro.csv')
    return df

def decorator_log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("execution_logs.txt", "a") as file:
            file.write(f'Function {func.__name__} executed in {total_time:.2f} seconds at {timestamp}')
        return result
    return wrapper

#-------------------------------------------------------------Réponses par académies par années------------------------------------------------------------------#


def display_reponses_par_academies_par_annee(df):

    st.subheader("Plot Du Nombre de réponses par académies :classical_building:")
    annees = df["annee"].unique()
    selected_annees = st.multiselect("Sélectionnez les années (academie)", annees, annees) #Crée un multiselect pour pouvoir sélectionner plusieurs années
    df_reponses_par_academie_par_annee = df[df["annee"].isin(selected_annees)].groupby("academie")["nombre_de_reponses"].sum().reset_index()
    fig = px.bar(df_reponses_par_academie_par_annee, x="academie", y="nombre_de_reponses", title="Nombre de Réponses par Académie")
    st.plotly_chart(fig)
    st.markdown("On peut voir ici que les académies de Lille, Lyon et Paris possèdent un grand nombre de réponses. La Corse, Limoges, la Réunion, la Guadeloupe quant à eux possèdent très peu de réponses.")

#-------------------------------------------------------------Réponses par domaine par années------------------------------------------------------------------#


def display_Reponses_Domaine_Annee(df):
    st.subheader("Plot Du Nombre de réponses par domaine :green_book:")
    annees = df["annee"].unique()
    selected_annees = st.multiselect("Sélectionnez les années (domaine)", annees, annees)
    df_reponses_par_domaine_par_annee = df[df["annee"].isin(selected_annees)].groupby("domaine")["nombre_de_reponses"].sum().reset_index()
    fig = px.bar(df_reponses_par_domaine_par_annee, x="domaine",y="nombre_de_reponses", title="Nombre de Réponses par domaine")
    st.plotly_chart(fig)

    st.markdown("On peut voir ici, un grand nombre de réponses dans le domaine du droit et assez peu en Lettres sur chaque année.")

    st.subheader("Plot Du Nombre de réponses par domaine :green_book:")

    def format_number(num):
        if num < 1000:
            return str(num)
        elif num < 1000000:
            return f'{num / 1000:.2f}K'
        else:
            return f'{num / 1000000:.2f}M'
        
    annees = df["annee"].unique()
    selected_annees = st.multiselect("Sélectionnez les années (domaine)", annees, annees, key='test')
    df_reponses_par_domaine_par_annee = df[df["annee"].isin(selected_annees)].groupby("domaine")["nombre_de_reponses"].sum().reset_index()

    st.bar_chart(df_reponses_par_domaine_par_annee, x="domaine", y = "nombre_de_reponses")

    st.markdown("On peut voir ici, un grand nombre de réponses dans le domaine du droit et assez peu en Lettres sur chaque année.")

#-------------------------------------------------------------Evolution Du Nombre de cadre par discipline------------------------------------------------------------------#

def display_evolution_cadre_discipline(df,annees) :

    st.subheader("Plot Evolution Du Nombre de cadre par discipline :notebook:")
    selected_annees = st.multiselect("Sélectionnez les années (cadres)", annees, annees)
    df_cadres_par_discipline_par_annee = df[df["annee"].isin(selected_annees)].groupby(["annee", "discipline"])["emplois_cadre"].sum().reset_index()

    #Les différents plots permettent de visualiser l'évolution de chacun au fil du temps, de les comparer également et d'avoir une vision sur la répartition de chaque disciplines par rapport aux autres
    plot_choice = st.radio("Select a Plot", ["Bar Chart 1", "Line Chart", "Bar Chart 2"])

    if plot_choice == "Bar Chart 1":
        fig = px.bar(df_cadres_par_discipline_par_annee, x="discipline",y="emplois_cadre", title="Nombre d'emplois cadre par discipline")
        st.plotly_chart(fig)

    elif plot_choice == "Line Chart":
        fig = px.line(df_cadres_par_discipline_par_annee, x="annee", y="emplois_cadre",color="discipline", title="Nombre d'emplois cadre par discipline")
        st.plotly_chart(fig)

    elif plot_choice == "Bar Chart 2":
        fig = px.bar(df_cadres_par_discipline_par_annee, x="annee", y="emplois_cadre",color="discipline", title="Nombre d'emplois cadre par discipline")
        st.plotly_chart(fig)

    st.markdown("Ces graphiques nous aident à mieux comprendre l'évolution du nombre de cadres par discipline au fil des années. Nous pouvons immédiatement constater que les domaines des sciences, de la technologie et de la santé demeurent les plus prédominants d'une année à l'autre. En revanche, les disciplines telles que l'histoire-géographie et les communications semblent avoir une nombre limité en termes de cadres. De plus, il est intéressant de noter qu'il y a eu une augmentation significative du nombre de cadres dans le domaine du droit depuis 2015.")
    st.markdown("On remarque légère augmentation du nombre de cadres entre 2016 et 2017.")

#------------------------------------------------------------- Taux d'insertion par discipline------------------------------------------------------------------#
def display_taux_insertion_par_discipline(df,annees) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    st.subheader("Plot Du Taux d'insertion par discipline :scroll:")

    selected_annees = st.multiselect("Sélectionnez les années", annees, annees, key="taux_insertion_par_discipline")

    df_insertion_par_disicpline_par_annee = df[df["annee"].isin(selected_annees)].groupby("discipline")["taux_dinsertion"].mean().reset_index()

    fig = px.bar(df_insertion_par_disicpline_par_annee, x="discipline", y="taux_dinsertion", title="Taux d'insertion par discipline")

    for i in range(len(df_insertion_par_disicpline_par_annee)):
        discipline = df_insertion_par_disicpline_par_annee.loc[i, "discipline"]
        taux_insertion = df_insertion_par_disicpline_par_annee.loc[i,"taux_dinsertion"]
        taux_insertion_percentage = f"{taux_insertion:.2f}%" #Ajout de l'annotation du taux d'insertion
        fig.add_annotation(
            x=discipline,
            y=taux_insertion,
            text=f"{taux_insertion_percentage}",
            showarrow=False,
            font=dict(size=9),
            yshift=12
        )

    st.plotly_chart(fig)

    st.markdown("Ce graphique nous dévoile les domaines d'études des masters présentant les taux d'insertion les plus élevés, à savoir l'enseignement, l'informatique, les sciences de l'ingénieur et le droit. À l'inverse, les domaines affichant les taux d'insertion les plus bas sont l'histoire-géographie et les sciences de la vie et de la terre. Ainsi, plus de 15 % d'étudiants qui n'ont pas trouvé d'emploi à la suite de leur formation. ")

#-------------------------------------------------------------Taux d'insertion par academie------------------------------------------------------------------#

def display_taux_insertion_par_academie(df,annees) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    st.subheader("Plot Du Taux d'insertion par academie :memo:")

    selected_annees = st.multiselect("Sélectionnez les années (academie)", annees, annees, key="taux_insertion_par_academie")

    df_insertion_par_academie_par_annee = df[df["annee"].isin(selected_annees)].groupby("academie")["taux_dinsertion"].mean().reset_index()

    fig = px.bar(df_insertion_par_academie_par_annee, x="academie",y="taux_dinsertion", title="Taux d'insertion par academie")

    for i in range(len(df_insertion_par_academie_par_annee)):
        academie = df_insertion_par_academie_par_annee.loc[i, "academie"]
        taux_insertion = df_insertion_par_academie_par_annee.loc[i,"taux_dinsertion"]
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

#-------------------------------------------------------------Taux d'insertion carte-----------------------------------------------------------------#

#Utilisation d'un geojson pour avoir le contour des académies
def taux_insertion_carte(df,annees) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    with open('academie.geojson') as f:
        geojson_data = json.load(f)

    selected_annees = st.multiselect("Sélectionnez les années", annees, annees, key="map_taux_insertion_par_academie")

    #Création des différents dataset en fonction de la variable à afficher 

    df_insertion_par_academie_par_annee = df[df["annee"].isin(selected_annees)].groupby("academie")["taux_dinsertion"].mean().reset_index()
    df_femmes_par_academie_par_annee = df[df["annee"].isin(selected_annees)].groupby("academie")["femmes"].mean().reset_index()
    df_salaire_median_par_academie_par_annee = df[df["annee"].isin(selected_annees)].groupby("academie")["salaire_net_median_des_emplois_a_temps_plein"].mean().reset_index()
    df_cadres_par_academie_par_annee = df[df["annee"].isin(selected_annees)].groupby("academie")["emplois_cadre"].mean().reset_index()
    df_emplois_stables_par_academie_par_annee = df[df["annee"].isin(selected_annees)].groupby("academie")["emplois_stables"].mean().reset_index()
    df_diplome_boursiers_par_academie_par_annee = df[df["annee"].isin(selected_annees)].groupby("academie")["de_diplomes_boursiers"].mean().reset_index()

    df_insertion_par_academie = df.groupby(["academie", "annee"])["taux_dinsertion"].mean().reset_index()
    df_salaire_par_academie = df.groupby(["academie", "annee"])["salaire_net_median_des_emplois_a_temps_plein"].mean().reset_index()
    df_femmes_par_academie = df.groupby(["academie", "annee"])["femmes"].mean().reset_index()
    df_cadres_par_academie = df.groupby(["academie", "annee"])["emplois_cadre"].mean().reset_index()
    df_emplois_stables_par_academie = df.groupby(["academie", "annee"])["emplois_stables"].mean().reset_index()
    df_diplome_boursiers_par_academie = df.groupby(["academie", "annee"])["de_diplomes_boursiers"].mean().reset_index()

    dataframes = {
        "taux_dinsertion": df_insertion_par_academie_par_annee,
        "salaire_net_median_des_emplois_a_temps_plein": df_salaire_median_par_academie_par_annee,
        "femmes": df_femmes_par_academie_par_annee,
        "emplois_stables": df_emplois_stables_par_academie_par_annee,
        "emplois_cadre": df_cadres_par_academie_par_annee,
        "de_diplomes_boursiers": df_diplome_boursiers_par_academie_par_annee,
    }

    dataframes_bins = {
        "taux_dinsertion": df_insertion_par_academie,
        'salaire_net_median_des_emplois_a_temps_plein': df_salaire_par_academie,
        'femmes': df_femmes_par_academie,
        "emplois_stables": df_emplois_stables_par_academie,
        "emplois_cadre": df_cadres_par_academie,
        "de_diplomes_boursiers": df_diplome_boursiers_par_academie,
    }

    column_to_display = st.selectbox("Selectionner la colonne à analyser par académie", list(dataframes.keys()))

    #Calcul du gap pour définir les bins, l'intervalle pour l'affichage
    selected_df = dataframes[column_to_display]
    selected_df_bins = dataframes_bins[column_to_display]
    min_value = selected_df_bins[column_to_display].min()
    max_value = selected_df_bins[column_to_display].max()
    gap = (max_value - min_value) / 7

    threshold_scale = [int(min_value + gap * i) for i in range(8)]
    if(threshold_scale[7] < max_value):
        threshold_scale[7] = max_value

    m = folium.Map(location=[48.8566, 2.3522], zoom_start=5)  # Centrer sur la France

    for feature in geojson_data['features']:
        academie = feature['properties']['name']
        tooltip = f'{academie}<br>' #Ajout des annotations
        value = selected_df[selected_df['academie']== academie][column_to_display].mean()
        tooltip += f'{column_to_display.replace("_", " ").capitalize()} : {value:.2f}'
        latitude, longitude = feature['properties']['geo_point_2d']
        folium.Marker(
            location=[latitude, longitude],
            tooltip=tooltip,
            icon=folium.DivIcon(
                icon_size=(20, 20),
                icon_anchor=(10, 10),
                html=f'<i class="fa fa-map-marker fa-2x" style="color: #61677A;"></i>' #Ajout d'une icone pour les annotations
            )
        ).add_to(m)

    #Chloropleth permet de diviser par couleurs les académies

    folium.Choropleth(
        geo_data=geojson_data,
        data=selected_df,
        columns=['academie', column_to_display],
        key_on='feature.properties.name',
        fill_color='Pastel1',
        fill_opacity=0.5,
        line_opacity=0.2,
        legend_name=column_to_display,
        threshold_scale=threshold_scale
    ).add_to(m)

    st.title(
        f'Carte des {column_to_display.replace("_", " ")} par Académie :world_map:')
    folium_static(m)

    st.markdown("- Cette carte fournit une représentation visuelle des différentes variables en fonction de l'académie, ce qui facilite leur compréhension")
    st.markdown("- Une analyse de la carte révèle que les régions situées au centre de la France affichent les taux d'insertion les plus élevés. Cependant, une comparaison entre 2012 et 2019 révèle un changement de tendance : en 2012, les académies de l'ouest et de l'est avaient des taux d'insertion plus élevés. En 2019, la tendance sest inversé, avec une concentration plus marquée d'emplois dans le centre.")
    st.markdown("- L'analyse des salaires révèle des rémunérations nettement plus élevées autour de Paris, ainsi qu'aux extrémités, telles que Lille, Nancy-Metz et Strasbourg. En revanche, la Corse présente les salaires les plus bas pour les emplois à temps plein. Une comparaison entre 2012 et 2019 indique une augmentation générale des salaires au fil du temps dans chaque ville.")
    st.markdown("- La part de femmes dans les emplois varie, avec une prédominance à Paris et à Dijon. En moyenne, cette part se situe entre 53 % et 65 %. Cependant, une comparaison entre 2012 et 2019 montre une diminution globale de la proportion de femmes.")
    st.markdown(
        "- Également, on observe une forte augmentation de la part d'emplois stables entre 2012 et 2019.")
    st.markdown("- Une tendance marquée est la forte hausse de la part d'emplois cadres en France. En 2012, elle se situait en moyenne entre 52 % et 62 %, mais en 2019, elle se situe principalement entre 62 % et 72 %")
    st.markdown("- En analysant la proportion de diplômes boursiers, on constate que Versailles présente très peu de diplômes boursiers, bien que le taux d'insertion y soit élevé et le taux de réponses moyen. Les taux les plus bas de diplômes boursiers se trouvent autour de Paris, tandis que les régions de l'est, de l'ouest et du sud affichent les taux les plus élevés. La comparaison entre 2012 et 2019 révèle une diminution de la part de diplômes boursiers au fil du temps")

    st.write("En somme, l'analyse montre que les régions situés au centre du pays semblent offrir de meilleures perspectives d'insertions professionnelles. Les salaires y sont également plus élevés. La forte augmentation de la part des emplois cadres suggère une tendance vers une économie plus axée sur les emplois qualifiés et professionnels. Enfin la diminution de la part de diplômes boursiers montre une évolutions dans les politiques de bourses.")

#-------------------------------------------------------------Taux de chomage par discipline ------------------------------------------------------------------#

def display_taux_chomage_discipline(df):

    df['taux_chomage'] = 100 - df['taux_dinsertion']
    df_chomage_par_discipline = df.groupby('discipline')['taux_chomage'].mean().reset_index()
    fig = px.bar(df_chomage_par_discipline, x='discipline',
                    y='taux_chomage', title='Taux de chomage par discipline')
    st.plotly_chart(fig)

    st.title('Taux de chomage par discipline (st.bar_chart)')
    st.bar_chart(df_chomage_par_discipline, x='discipline', y='taux_chomage')

    st.markdown("En observant ce barplot, , il est clair que les domaines d'études en lettres (comme l'histoire et les lettres) et les sciences sociales affichent des taux de chômage considérablement plus élevés. En revanche, les domaines de l'informatique et de l'enseignement présentent des taux de chômage nettement plus bas.")


#-------------------------------------------------------------Comparaison taux de chomage par discipline et taux chomage regional  ------------------------------------------------------------------#
def display_comparaison_chomage_regional_discipline_domaine(df):                                                                                                                                                                                                                                                                                                          
    df_chomage_par_discipline = df.groupby('discipline')['taux_chomage'].mean().reset_index()
    fig_discipline = px.bar(df_chomage_par_discipline, x='discipline', y='taux_chomage',title='Taux de chomage par discipline et Taux de chomage régional')
    fig_discipline.add_bar(x=df_chomage_par_discipline['discipline'], y=df['taux_de_chomage_regional'], name='Taux de chomage régional')
    fig_discipline.update_layout(barmode='group', xaxis_tickangle=-45, height=600, width=800) #Le group permet de comparer plus facilement les 2 variables par domaine
    df_chomage_par_domaine = df.groupby('domaine')['taux_chomage'].mean().reset_index()

    fig_domaine = px.bar(df_chomage_par_domaine, x='domaine', y='taux_chomage', title='Taux de chomage par domaine et Taux de chomage régional')
    fig_domaine.add_bar(x=df_chomage_par_domaine['domaine'], y=df['taux_de_chomage_regional'], name='Taux de chomage régional')
    fig_domaine.update_layout(barmode='group', xaxis_tickangle=-45, height=500, width=800)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_domaine)

    with col2:
        st.plotly_chart(fig_discipline)

    st.markdown("En comparant les taux de chômage par domaine d'études avec le taux de chômage régional, on peut observer des tendances intéressantes. Les domaines tels que les lettres, les langues et les sciences sociales ont un taux de chômage plus élevé que la moyenne régionale. En revanche, les domaines telles que l'enseignement, le droit et les sciences ont des taux de chômage inférieurs à la moyenne régionale. Une analyse plus approfondie révèle que les études littéraires, les sciences sociales et les sciences de la vie et de la terre présentent des taux de chômage nettement plus élevés que la moyenne régionale.")

#-------------------------------------------------------------Taux dinsertion par domaine et situation ------------------------------------------------------------------#
def display_taux_insertion_situation_domaine_discipline(df):                                                                                                                                                                                                                                                                                                                  
    df_avant_18_mois = df[df['situation'] == '18 mois après le diplôme']
    df_apres_18_mois = df[df['situation'] == '30 mois après le diplôme']

    df_avant_18_mois_domaine = df_avant_18_mois.groupby(
        'domaine')['taux_dinsertion'].mean().reset_index()
    df_apres_18_mois_domaine = df_apres_18_mois.groupby(
        'domaine')['taux_dinsertion'].mean().reset_index()

    fig_situation_domaine = px.bar(df_avant_18_mois_domaine, x='domaine',y='taux_dinsertion', title='Taux dinsertion par domaine et situation')
    fig_situation_domaine.update_traces(marker_color="#F2D8D8")
    fig_situation_domaine.add_bar(x=df_apres_18_mois_domaine['domaine'], y=df['taux_dinsertion'], name='Taux dinsertion après 18 mois')

    fig_situation_domaine.update_traces(marker_color="#EF9595", selector={"name": "Taux dinsertion après 18 mois"})
    fig_situation_domaine.update_layout(barmode='group', xaxis_tickangle=-45, height=600, width=800, showlegend=True)

#-------------------------------------------------------------Taux dinsertion par discipline et situation ------------------------------------------------------------------#

    df_avant_18_mois_discipline = df_avant_18_mois.groupby('discipline')['taux_dinsertion'].mean().reset_index()
    df_apres_18_mois_discipline = df_apres_18_mois.groupby('discipline')['taux_dinsertion'].mean().reset_index()

    fig_situation_discipline = px.bar(df_avant_18_mois_discipline, x='discipline',y='taux_dinsertion', title='Taux dinsertion par domaine et situation')
    fig_situation_discipline.update_traces(marker_color="#F2D8D8")
    fig_situation_discipline.add_bar(x=df_apres_18_mois_discipline['discipline'], y=df['taux_dinsertion'], name='Taux dinsertion après 18 mois')
    fig_situation_discipline.update_traces(marker_color="#EF9595", selector={"name": "Taux dinsertion après 18 mois"})
    fig_situation_discipline.update_layout(barmode='group', xaxis_tickangle=-45, height=700, width=800)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_situation_domaine)

    with col2:
        st.plotly_chart(fig_situation_discipline)

    st.markdown("Ce graphique suggère que la majorité des domaines d'études semblent offrir des perspectives d'insertion professionnelle positives au cours des 18 premiers mois après l'obtention du diplôme avec une situation relativement équilibrée dans le domaine des lettres. Cependant, il est important de noter que des tendances différentes se dégagent pour certains domaines spécifiques. Par exemple, les domaines tels que la technologie, l'histoire-géographie, l'informatique, les sciences de la vie et de la terre montrent généralement des signes d'insertion professionnelle qui se produisent après cette période de 18 mois. D'un autre côté, pour les domaines comme la gestion, le droit et la communication, on constate que l'insertion professionnelle se passe généralement pendant la période des 18 mois. ")

#------------------------------------------------------------- Plot Etudiants extérieurs région par discipline ------------------------------------------------------------------#

def display_etudiants_exterieurs_region_discipline(df) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    df["nombre_emplois"] = df["nombre_de_reponses"]*df["taux_dinsertion"]/100
    df_region_discipline = df.groupby('discipline')[['emplois_exterieurs_a_la_region_de_luniversite', 'nombre_emplois']].sum().reset_index()
    fig = px.bar(df_region_discipline, x='discipline', y='nombre_emplois',title="Etudiants travaillant à l'extérieur de leur région universitaire par discipline")
    fig.update_traces(marker_color="#A73121")
    fig.add_bar(x=df_region_discipline['discipline'], y=df_region_discipline['emplois_exterieurs_a_la_region_de_luniversite'], name='Emplois exterieurs à la région')
    fig.update_traces(marker_color="#FFC090", selector={"name": "Emplois exterieurs à la région"})
    fig.update_layout(barmode='group', xaxis_tickangle=-45, height=600, width=1000)

    st.plotly_chart(fig)

    st.markdown("On peut remarquer ici que la plupart des étudiants préfèrent rester dans leurs régions d'études indépendamment de leurs discipline, ce qui indique une tendance à la localité.")

#-------------------------------------------------------------Plot Etudiants extérieurs région par région académique ------------------------------------------------------------------#

def display_etudiants_exterieurs_region_academie(df) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    df["nombre_emplois"] = df["nombre_de_reponses"]*df["taux_dinsertion"]/100
    df_region = pd.read_csv('academie_region.csv', delimiter=";")
    df_region_acad = pd.merge(df, df_region, on='academie', how='inner')
    df_exterieurs_acad = df_region_acad.groupby('region')[['emplois_exterieurs_a_la_region_de_luniversite', 'nombre_emplois']].sum().reset_index()
    fig = px.bar(df_exterieurs_acad, x='region', y='nombre_emplois',title="Etudiants travaillant à l'extérieur de leur région universitaire par region académique")
    fig.update_traces(marker_color="#A73121")
    fig.add_bar(x=df_exterieurs_acad['region'], y=df_exterieurs_acad['emplois_exterieurs_a_la_region_de_luniversite'], name='Emplois exterieurs à la région')
    fig.update_traces(marker_color="#FFC090", selector={"name": "Emplois exterieurs à la région"})
    fig.update_layout(barmode='group', xaxis_tickangle=-45, height=600, width=1000)

    st.plotly_chart(fig)
    st.markdown("On remarque que la plupart des étudiants préfèrent rester dans leurs régions d'études, ce qui indique une tendance à la localité. Toutefois, dans le cas des régions ultramarines, on constate généralement que ces étudiants ont davantage tendance à chercher des opportunités de travail dans d'autres régions. Cette dynamique pourrait s'expliquer par le fait que ces régions offrent peut-être moins d'opportunités d'emploi dans leur domaine d'études, les incitant ainsi à se déplacer vers d'autres régions.")

#-------------------------------------------------------------Taux de femmes par discipline------------------------------------------------------------------#
def display_femmes_discipline(df) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    st.subheader("Taux de femmes par discipline")

    discipline = st.selectbox('Choisissez une discipline', df['discipline'].unique())

    df_filtered = df[df['discipline'] == discipline]

    femmes = df_filtered['femmes'].mean()
    hommes = 100 - femmes

    st.write(f"Taux de femmes : {femmes}%")
    st.write(f"Taux d'hommes : {hommes}%")

    # Création du pie chart
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie([femmes, hommes], labels=['Femmes', 'Hommes'], colors=['#e69adf', '#91b6f2'], autopct='%1.1f%%')
    plt.title('Répartition par sexe')
    st.pyplot(fig)
    
#-------------------------------------------------------------Taux de femmes avec le temps------------------------------------------------------------------#

def display_femmes_temps(df) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    st.subheader("Taux de femmes avec le temps")
    
    annees = df["annee"].unique()
    selected_annees = st.multiselect("Sélectionnez les années", annees,annees)
    
    df_femmes_par_discipline_par_annee = df[df["annee"].isin(selected_annees)].groupby(["annee", "discipline"])["femmes"].mean().reset_index()

    fig = px.line(df_femmes_par_discipline_par_annee, x="annee", y="femmes", color="discipline", title="Taux de femmes par discipline et par année")
    st.plotly_chart(fig)

    df_femmes_par_annee = df[df["annee"].isin(selected_annees)].groupby(["annee"])["femmes"].mean().reset_index()
    fig = px.line(df_femmes_par_annee, x="annee", y="femmes", title="Taux de femmes total par année")
    fig.update_yaxes(range=[30, 70])
    st.plotly_chart(fig)

    st.markdown("Attention : un pourcentage moyen de femmes plus élevé ne veut pas dire qu'il y a plus de femmes que d'hommes au sein des universités.")
    st.markdown("Exemple : il y a 90% de femmes en psychologie, et 10% de femmes en informatique. Seulement, si il y a 10000 étudiants en informatique et 500 étudiants en psychologie, alors il y aura toujours plus d'hommes que de femmes.")
    st.markdown("On remarque que le taux de femmes chute complètement au fil des années dans les disciplines des sciences fondamentales et sciences, technologies et santé. On observe légèrement plus de femmes au contraire dans les disciplines juridiques. Malheureusement, le dataset ne nous permet pas de comprendre pourquoi les femmes boudent les compétences scientifiques :pensive:")

#-------------------------------------------------------------Check corrélations entre le taux de femmes et les autres taux------------------------------------------------------------------#

def display_correlation_femme_variables(df) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    st.subheader("A quel point le taux de femmes est corrélé avec les autres valeurs de notre dataset ?")

    df1 = df.dropna(subset=['femmes', 'emplois_cadre', 'taux_dinsertion', 'emplois_stables', 'emplois_a_temps_plein', 'salaire_net_median_des_emplois_a_temps_plein']) # Il y a un problème dans le scatter si une des trois colonnes est NaN
    df1['femmes'] = df1['femmes'] / 100
    
    variables = ['emplois_cadre', 'taux_dinsertion', 'emplois_stables', 'emplois_a_temps_plein', 'salaire_net_median_des_emplois_a_temps_plein']
    for var in variables:
        df1[var] = df1[var] / 100

    variable = st.selectbox('Choisissez une variable', variables)

    # Création du scatter plot avec ligne de régression
    plt.figure(figsize=(10, 6))
    sns.regplot(x='femmes', y=variable, data=df1, scatter_kws={'s': 2, 'color': '#e08610'}, line_kws={'color': '#8548ab'})
    plt.title(f'Corrélation entre le nombre de femmes et le nombre de {variable}')
    plt.xlabel('Taux de femmes')
    plt.ylabel(f'Taux de {variable}')
    st.pyplot(plt)

    st.markdown("Malheureusement, on remarque que toutes les droites de régression vont dans le même sens : plus il y a de femmes dans une filière, moins le salaire à la sortie est ahaut. Il en va de même pour le taux d'insertion, le taux d'emplois stables et le taux d'emplois à temps plein... La pente est d'autant plus importante pour les salaires.", unsafe_allow_html=True)
#-------------------------------------------------------------Taux de femmes par discipline------------------------------------------------------------------#
def display_femmes_discipline(df) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    st.subheader("Taux de femmes par discipline")
    discipline = st.selectbox('Choisissez une discipline', df['discipline'].unique())

    df_filtered = df[df['discipline'] == discipline]

    femmes = df_filtered['femmes'].mean()
    hommes = 100 - femmes

    st.write(f"Taux de femmes : {femmes}%")
    st.write(f"Taux d'hommes : {hommes}%")

    # Création du pie chart
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie([femmes, hommes], labels=['Femmes', 'Hommes'],
            colors=['#e69adf', '#91b6f2'], autopct='%1.1f%%')
    plt.title('Répartition par sexe')
    st.pyplot(fig)
#-------------------------------------------------------------Taux de femmes avec le temps------------------------------------------------------------------#

def display_femmes_temps(df) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    st.subheader("Taux de femmes avec le temps")

    annees = df["annee"].unique()
    selected_annees = st.multiselect("Sélectionnez les années", annees, annees)

    df_femmes_par_discipline_par_annee = df[df["annee"].isin(selected_annees)].groupby(["annee", "discipline"])["femmes"].mean().reset_index()

    fig = px.line(df_femmes_par_discipline_par_annee, x="annee", y="femmes",color="discipline", title="Taux de femmes par discipline et par année")
    st.plotly_chart(fig)

    df_femmes_par_annee = df[df["annee"].isin(selected_annees)].groupby(["annee"])["femmes"].mean().reset_index()
    fig = px.line(df_femmes_par_annee, x="annee", y="femmes",title="Taux de femmes total par année")
    fig.update_yaxes(range=[30, 70])
    st.plotly_chart(fig)

    st.line_chart(df_femmes_par_annee.set_index("annee")["femmes"])
    st.title("Taux de femmes total par année")

#-------------------------------------------------------------Check corrélations entre le taux de femmes et les autres taux------------------------------------------------------------------#

def display_correlation_femme_variables(df) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    st.subheader("A quel point le taux de femmes est corrélé avec les autres valeurs de notre dataset ?")

    # Il y a un problème dans le scatter si une des trois colonnes est NaN
    df1 = df.dropna(subset=['femmes', 'emplois_cadre','taux_dinsertion', 'emplois_stables', 'emplois_a_temps_plein'])

    # Conversion des pourcentages en nombres décimaux
    df1['femmes'] = df1['femmes'] / 100

    variables = ['emplois_cadre', 'taux_dinsertion','emplois_stables', 'emplois_a_temps_plein']
    for var in variables:
        df1[var] = df1[var] / 100

    variable = st.selectbox('Choisissez une variable', variables)

    # Création du scatter plot avec ligne de régression
    plt.figure(figsize=(10, 6))
    sns.regplot(x='femmes', y=variable, data=df1, scatter_kws={'s': 2, 'color': '#e08610'}, line_kws={'color': '#8548ab'})
    plt.title(f'Corrélation entre le nombre de femmes et le nombre de {variable}')
    plt.xlabel('Taux de femmes')
    plt.ylabel(f'Taux de {variable}')
    st.pyplot(plt)

    st.markdown("Malheureusement, on remarque que toutes les droites de régression vont dans le même sens : plus il y a de femmes dans une filière, moins le salaire à la sortie est ahaut. Il en va de même pour le taux d'insertion, le taux d'emplois stables et le taux d'emplois à temps plein...", unsafe_allow_html=True)

#-------------------------------------------------------------Histogrammes par académie------------------------------------------------------------------#

def display_histogramme_academie(df, academie_list) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    st.subheader("Histogrammes des salaires par académie.")
    
    selected_academie = st.selectbox("Sélectionnez une académie :", academie_list)

    # Filtrer les données pour l'académie sélectionnée
    filtered_df = df[df['academie'] == selected_academie]

    # Créer un histogramme des salaires
    fig, ax = plt.subplots()
    ax.hist(filtered_df['salaire_net_median_des_emplois_a_temps_plein'], bins=20, color='skyblue', edgecolor='black')
    ax.set_xlabel("Salaire Net Médian (par mois)")
    ax.set_ylabel("Nombre d'Observations")
    ax.set_title(f"Histogramme des Salaires pour l'académie de {selected_academie}")

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)

    st.markdown("Il existe une corrélation entre les catégories de richesse des régions des académies et les salaires. Par exemple, le salaire médian est plus important en sortie d'académies Parisiennes et plus faible en sortie d'académies Corses. Le dataset ne nous permet pas de quantifier cette corrélation précisément.")

#-------------------------------------------------------------Histogrammes par discipline------------------------------------------------------------------#

def display_histogram_discipline(df,discipline_list) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    st.subheader("Histogrammes des salaires par discipline.")

    selected_discipline = st.selectbox("Sélectionnez une discipline :", discipline_list)

    # Filtrer les données pour l'académie sélectionnée
    filtered_df = df[df['discipline'] == selected_discipline]

    # Créer un histogramme des salaires
    fig, ax = plt.subplots()
    ax.hist(filtered_df['salaire_net_median_des_emplois_a_temps_plein'], bins=20, color='#fcba03', edgecolor='black')
    ax.set_xlabel("Salaire Net Médian (par mois)")
    ax.set_ylabel("Nombre d'Observations")
    ax.set_title(f"Histogramme des Salaires pour la discipline : {selected_discipline}")

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)

    st.markdown("Visiblement, les disicplines de sciences 'dures' et de droit gagnent plus que les disciplines d'enseignement et de sciences sociales.")
    # Afficher le graphique dans Streamlit
    st.pyplot(fig)

#-------------------------------------------------------------Barplots par discipline et académie------------------------------------------------------------------#
def display_barplot_par_acad_discipline(df, discipline_list, academie_list):
    st.subheader("Salaires médians par discipline et par académie.")
    
    academie_selectionnee = st.selectbox('Sélectionnez une académie:', academie_list)
    df_filtre = df[df['academie'] == academie_selectionnee]

    fig, ax = plt.subplots()

    for discipline in discipline_list:
        df_discipline = df_filtre[df_filtre['discipline'] == discipline]
        salaire_moyen = df_discipline['salaire_net_median_des_emplois_a_temps_plein'].mean()
        ax.barh(discipline, salaire_moyen)

    ax.set_xlabel('Salaire moyen')
    ax.set_ylabel('Discipline')
    st.pyplot(fig)

    
#-------------------------------------------------------------Est-ce que les pauvres restent pauvres ?------------------------------------------------------------------#
def display_pauvres(df):
    st.subheader("Est-ce que les filières avec beaucoup d'étudiants boursiers ont un salaire médian plus bas ?")

    df2 = df.dropna(subset=['salaire_net_median_des_emplois_a_temps_plein', 'de_diplomes_boursiers'])

    plt.figure(figsize=(10, 6))
    sns.regplot(x='de_diplomes_boursiers', y='salaire_net_median_des_emplois_a_temps_plein', data=df2, scatter_kws={'s': 2, 'color': '#e08610'}, line_kws={'color': '#8548ab'})
    plt.title("Corrélation entre le taux de boursiers et les salaires")
    plt.xlabel('Taux de boursiers')
    plt.ylabel('Salaires')
    st.pyplot(plt)

    st.markdown("La courbe de régression montre que plus il y a d'étudiants boursiers dans une formation, plus le salaire en sortie d'études est bas. On peut tirer différentes conclusions de cette observation : est-ce qu'il existe réellement une notion de mérite, si un élève boursier gagne moins qu'un autre élève qui se forme dans la même discipline, au sein de deux formations publiques ?")

#-------------------------------------------------------------MAIN FUNCTION -----------------------------------------------------------------#

@decorator_log_time
def main():
    
    st.header("Plotting Data")
    df = load_data()
    st.write("Notre DataSet")
    st.dataframe(df)

    st.sidebar.title("Menu de Navigation")
    choix = st.sidebar.radio("Sélectionnez une option", ["Nombre de Réponse", "Insertion Post-Diplome", "Impact du genre", "Salaires"])

    if choix == "Nombre de Réponse":
        st.write("Sur cette page, nous examinerons le nombre de réponses reçues afin de déterminer les groupes de données les plus représentatifs.")
        display_reponses_par_academies_par_annee(df)
        display_Reponses_Domaine_Annee(df)

    elif choix == "Insertion Post-Diplome":

        st.subheader("Insertion Post-Diplome")
        annees = df["annee"].unique()
        display_evolution_cadre_discipline(df,annees)
        display_taux_insertion_par_discipline(df,annees)
        display_taux_insertion_par_academie(df,annees)
        taux_insertion_carte(df,annees)
        display_taux_chomage_discipline(df)
        display_comparaison_chomage_regional_discipline_domaine(df)
        display_taux_insertion_situation_domaine_discipline(df)
        display_etudiants_exterieurs_region_discipline(df)
        display_etudiants_exterieurs_region_academie(df)

    elif choix == "Impact du genre":
        st.header("Impact du genre : est-ce que le fait d'être une femme a un impact sur la discipline que l'on va étudier, sur notre salaire ?")
        display_femmes_discipline(df)
        display_femmes_temps(df)
        display_correlation_femme_variables(df)

    elif choix == "Salaires":

        st.header("Qu'est-ce qui impacte les salaires ?")
        academie_list = df['academie'].unique()
        discipline_list = df['discipline'].unique()
        display_histogramme_academie(df, academie_list)
        display_histogram_discipline(df,discipline_list)
        display_barplot_par_acad_discipline(df, discipline_list, academie_list)
        display_pauvres(df)
   
if __name__ == '__main__':
    main()