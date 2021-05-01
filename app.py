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

choice = st.sidebar.radio("Select a visualization to display", ('Total Ecological footprint/biocapacity',
                                                        'Per Capita Ecological footprint/biocapacity'))
if choice == 'Total Ecological footprint/biocapacity':
    option = st.multiselect('What countries do you want to display?', df_countries_totals['Country'], key='viz1')
    df_selected = df_countries_totals.loc[df_countries_totals['Country'].isin(option)]

    # Plotting Total Ecological Footprint
    footprint = alt.Chart(df_selected).transform_fold(
        ['Cropland Footprint', 'Grazing Footprint', 'Forest Footprint', 'Carbon Footprint', 'Fish Footprint',
         'No Footprint Component Data'],
        as_=['Footprint', 'Total Ecological Footprint']
    ).mark_bar().encode(
        y=alt.X('Country:N', sort='-x'),
        x=alt.Y('Total Ecological Footprint:Q', title='Total Ecological Footprint (in millions of gha)'),
        color='Footprint:N'
    ).interactive()

    footprint.save('footprint.html')
    HtmlFile = open('footprint.html')
    source_code = HtmlFile.read()
    components.html(source_code, height=300, width=850)

    # Plotting total Biocapacity
    biocapacity = alt.Chart(df_selected).transform_fold(
        ['Cropland', 'Grazing Land', 'Forest Land', 'Fishing Water', 'Urban Land', 'No Biocapacity Component Data'],
        as_=['Biocapacity', 'Total Biocapacity']
    ).mark_bar().encode(
        y=alt.X('Country:N', sort='-x'),
        x=alt.Y('Total Biocapacity:Q', title='Total Biocapacity (in millions of gha)'),
        color='Biocapacity:N'
    ).interactive()

    biocapacity.save('biocapacity.html')
    HtmlFile = open('biocapacity.html')
    source_code = HtmlFile.read()
    components.html(source_code, height=300, width=850)

if choice == 'Per Capita Ecological footprint/biocapacity':
    option = st.multiselect('What countries do you want to display?', df_countries['Country'], key='viz2')
    df_selected = df_countries.loc[df_countries['Country'].isin(option)]

    footprint_per_capita = (alt.Chart(df_selected).transform_fold(
        ['Cropland Footprint', 'Grazing Footprint', 'Forest Footprint', 'Carbon Footprint', 'Fish Footprint',
         'No Footprint Component Data'],
        as_=['Footprint', 'Total Ecological Footprint (per capita)']
    ).mark_bar().encode(
        y=alt.X('Country:N', sort='-x'),
        x=alt.Y('Total Ecological Footprint (per capita):Q', title='Per Capita Biocapacity (in gha)'),
        color='Footprint:N'
    ).interactive())

    # ).mark_bar().encode(
    #     x=alt.X('Country:N', sort='-y'),
    #     y='Total Ecological Footprint (per capita):Q',
    #     color='Footprint:N'
    # ).interactive()



    # st.write(footprint_per_capita)
    #The code below is an alternative to st.write(footprint_per_capita).
    #Issues arose when calling that function, so instead I wrote the bar chart to an HTML file,
    #then rendered that HTML file in Streamlit.
    footprint_per_capita.save('footprint_per_capita.html')
    HtmlFile = open('footprint_per_capita.html')
    source_code = HtmlFile.read()
    components.html(source_code, height=250, width=850)


    biocapacity_per_capita = alt.Chart(df_selected).transform_fold(
        ['Cropland', 'Grazing Land', 'Forest Land', 'Fishing Water', 'Urban Land', 'No Biocapacity Component Data'],
        as_=['Biocapacity', 'Total Biocapacity (per capita)']
    ).mark_bar().encode(
        y=alt.X('Country:N', sort='-x'),
        x=alt.Y('Total Biocapacity (per capita):Q', title='Per Capita Ecological Footprint (in gha)'),
        color='Biocapacity:N'
    ).interactive()

    biocapacity_per_capita.save('biocapacity_per_capita.html')
    HtmlFile = open('biocapacity_per_capita.html')
    source_code = HtmlFile.read()
    components.html(source_code, height=250, width=850)