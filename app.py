import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import streamlit.components.v1 as components
from vega_datasets import data

@st.cache
def load_data():
    #Loading pre-processed data
    df_countries = pd.read_csv('countries_per_capita.csv')
    df_countries_totals = pd.read_csv('countries_total.csv')
    country_data = pd.read_csv('country_data.csv')
    return df_countries, df_countries_totals, country_data

df_countries, df_countries_totals, country_data = load_data()

container = st.beta_container()

choice = st.sidebar.radio("Select a visualization to display", ('Total Ecological footprint/biocapacity',

                                                        'Per Capita Ecological footprint/biocapacity', 'Regression analysis', 'Biocapacity deficit/reserve', 'Ecological Footprint Map'))
st.title('Analysis on the 2016 Ecological Footprint Dataset')
if choice == 'Total Ecological footprint/biocapacity':
    col1, col2 = st.beta_columns(2)

    with col1:
        st.header('Total Ecological Footprint')

        top_countries_count = st.selectbox('How many top countries would you like to show?', (5, 10, 15), key='viz2')

        if top_countries_count:
            option = st.multiselect('What countries do you want to display?', df_countries_totals['Country'].tolist(), df_countries_totals['Country'][0:top_countries_count].tolist(), key='viz1')
        else:
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

        st.altair_chart(footprint, use_container_width=True)

    # footprint.save('footprint.html')
    # HtmlFile = open('footprint.html')
    # source_code = HtmlFile.read()
    # components.html(source_code, height=300, width=850)

    # Plotting total Biocapacity
    with col2:
        st.header('Total Biocapacity')

        top_countries_count = st.selectbox('How many top countries would you like to show?', (5, 10, 15), key='viz1')

        if top_countries_count:
            option = st.multiselect('What countries do you want to display?', df_countries_totals['Country'].tolist(),
                                    df_countries_totals.sort_values(by='Total Biocapacity', ascending=False)['Country'][0:top_countries_count].tolist(), key='viz2')
        else:
            option = st.multiselect('What countries do you want to display?', df_countries_totals['Country'],
                                    key='viz2')
        df_selected1 = df_countries_totals.loc[df_countries_totals['Country'].isin(option)]
        #Horizontal
        biocapacity = alt.Chart(df_selected1).transform_fold(
            ['Cropland', 'Grazing Land', 'Forest Land', 'Fishing Water', 'Urban Land', 'No Biocapacity Component Data'],
            as_=['Biocapacity', 'Total Biocapacity']
        ).mark_bar().encode(
            y=alt.X('Country:N', sort='-x'),
            x=alt.Y('Total Biocapacity:Q', title='Total Biocapacity (in millions of gha)'),
            color='Biocapacity:N'
        ).interactive()

        st.altair_chart(biocapacity, use_container_width=True)

    # biocapacity.save('biocapacity.html')
    # HtmlFile = open('biocapacity.html')
    # source_code = HtmlFile.read()
    # components.html(source_code, height=300, width=850)

if choice == 'Per Capita Ecological footprint/biocapacity':
    col1, col2 = st.beta_columns(2)

    with col1:
        st.header('Per Capita Ecological Footprint')

        top_countries_count = st.selectbox('How many top countries would you like to show?', (5, 10, 15), key='viz3')

        if top_countries_count:
            option = st.multiselect('What countries do you want to display?', df_countries['Country'].tolist(),
                                    df_countries['Country'][0:top_countries_count].tolist(), key='viz3')
        else:
            option = st.multiselect('What countries do you want to display?', df_countries['Country'],
                                    key='viz3')

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

        st.altair_chart(footprint_per_capita, use_container_width=True)

    with col2:
        st.header('Per Capita Biocapacity')

        top_countries_count = st.selectbox('How many top countries would you like to show?', (5, 10, 15), key='viz4')

        if top_countries_count:
            option = st.multiselect('What countries do you want to display?', df_countries['Country'].tolist(),
                                    df_countries.sort_values(by='Total Biocapacity', ascending=False)['Country'][
                                    0:top_countries_count].tolist(), key='viz4')
        else:
            option = st.multiselect('What countries do you want to display?', df_countries['Country'],
                                    key='viz4')

        df_selected1 = df_countries_totals.loc[df_countries['Country'].isin(option)]

        biocapacity_per_capita = alt.Chart(df_selected1).transform_fold(
            ['Cropland', 'Grazing Land', 'Forest Land', 'Fishing Water', 'Urban Land', 'No Biocapacity Component Data'],
            as_=['Biocapacity', 'Total Biocapacity (per capita)']
        ).mark_bar().encode(
            y=alt.X('Country:N', sort='-x'),
            x=alt.Y('Total Biocapacity (per capita):Q', title='Per Capita Ecological Footprint (in gha)'),
            color='Biocapacity:N'
        ).interactive()

        st.altair_chart(biocapacity_per_capita, use_container_width=True)


if choice == 'Regression analysis':
    #col1, col2 = st.beta_columns(2)

    #with col1:
    base = alt.Chart(df_countries).mark_circle(size=60).encode(
        x='HDI',
        y=alt.Y('Total Ecological Footprint', title='Per Capita Ecological Footprint'),
        color='Region:N',
        tooltip=['Country', 'Region', alt.Tooltip('Total Ecological Footprint', title='Ecological Footprint'),
                 'HDI']
    ).properties(
        title='Per Capita Ecological Footprint vs. HDI'
    )

    exp = base + base.transform_regression("HDI", "Total Ecological Footprint", method="exp", as_=['HDI', 'exponential']).mark_line().transform_fold(["exponential"], as_=["Regression", "Total Ecological Footprint"]).encode(alt.Color("Regression:N"))
    exp = exp.interactive()
    st.altair_chart(exp, use_container_width=True)

    #with col2:
    base1 = alt.Chart(df_countries).mark_circle(size=60).encode(
        x='GDP per Capita',
        y=alt.Y('Total Ecological Footprint', title='Per Capita Ecological Footprint'),
        color='Region:N',
        tooltip=['Country', 'Region', alt.Tooltip('Total Ecological Footprint', title='Ecological Footprint'),
                 'GDP per Capita']
    ).properties(
        title='Per Capita Ecological Footprint vs. GDP per Capita'
    )

    log = base1 + base1.transform_regression("GDP per Capita", "Total Ecological Footprint", method="log", as_=['GDP per Capita', 'log']).mark_line().transform_fold(["log"], as_=["Regression", "Total Ecological Footprint"]).encode(alt.Color("Regression:N"))
    log = log.interactive()
    st.altair_chart(log, use_container_width=True)

if choice == 'Biocapacity deficit/reserve':
    biocapacity_order = st.selectbox('Would you like to see the countries with the largest deficits or reserves?', ('Deficits', 'Reserves'), key='viz5')

    top_countries_count = st.selectbox('How many countries would you like to show?', (5, 10, 15), key='viz5')

    if top_countries_count and biocapacity_order:
        option = st.multiselect('What countries do you want to display?', df_countries['Country'].tolist(),
                                df_countries.sort_values(by='Biocapacity Deficit or Reserve', ascending=(biocapacity_order=='Deficits'))['Country'][
                                0:top_countries_count].tolist(), key='viz5')
    else:
        option = st.multiselect('What countries do you want to display?', df_countries_totals['Country'],
                                key='viz5')
    df_selected1 = df_countries.loc[df_countries['Country'].isin(option)]

    def_reserve = alt.Chart(df_selected1).mark_bar().encode(
        x=alt.X("Country:N", sort='y'),
        y="Biocapacity Deficit or Reserve:Q",
        color=alt.condition(
            alt.datum['Biocapacity Deficit or Reserve'] > 0,
            alt.value("steelblue"),  # The positive color
            alt.value("orange")  # The negative color
        )
    )

    def_reserve = def_reserve.interactive()
    def_reserve

if choice == 'Ecological Footprint Map':
    country_positions = alt.topo_feature(data.world_110m.url, 'countries')

    world_map = alt.Chart(country_positions).mark_geoshape().encode(
        color='Footprint per capita:Q'
        , tooltip=['Country:N', 'Footprint per capita:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(country_data, 'id', ['Footprint per capita', 'Country'])
    ).project(
        type='equirectangular'
    ).properties(
        width=600,
        height=400,
        title='Ecological Footprint Choropleth Map'
    )

    world_map = st.altair_chart(world_map, use_container_width=True)