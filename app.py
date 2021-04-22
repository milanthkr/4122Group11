import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import streamlit.components.v1 as components

@st.cache
def load_data():
    #Loading pre-processed data
    df_countries = pd.read_csv('countries_per_capita.csv')
    df_countries_totals = pd.read_csv('countries_total.csv')
    return df_countries, df_countries_totals


df_countries, df_countries_totals = load_data()

option = st.multiselect('What countries do you want to display?', df_countries['Country'])
print(option)
df_selected = df_countries.loc[df_countries['Country'].isin(option)]

footprint_per_capita = (alt.Chart(df_selected).transform_fold(
    ['Cropland Footprint', 'Grazing Footprint', 'Forest Footprint', 'Carbon Footprint', 'Fish Footprint',
     'No Footprint Component Data'],
    as_=['Footprint', 'Total Ecological Footprint (per capita)']
).mark_bar().encode(
    y=alt.X('Country:N', sort='-x'),
    x='Total Ecological Footprint (per capita):Q',
    color='Footprint:N'
).interactive())


# st.write(footprint_per_capita)
#The code below is an alternative to st.write(footprint_per_capita).
#Issues arose when calling that function, so instead I wrote the bar chart to an HTML file,
#then rendered that HTML file in Streamlit.
footprint_per_capita.save('footprint_per_capita.html')
HtmlFile = open('footprint_per_capita.html')
source_code = HtmlFile.read()
components.html(source_code, height = 800)

#Other viz's
#biocapacity_per_capita
#footprint_total =
#biocapacity_total =



