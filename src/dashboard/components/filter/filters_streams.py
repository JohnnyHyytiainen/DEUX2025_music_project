import streamlit as st


def continent_filter(continents):
    col = st.columns(3)
    with col[2]:
        if st.button("Europe", width=700):
            st.session_state.continent = "Europe"
    with col[0]:
        if st.button("Asia", width=700):
            st.session_state.continent = "Asia"
    with col[1]:
        if st.button("Africa", width=700):
            st.session_state.continent = "Africa"
    with col[2]:
        if st.button("Oceania", width=700):
            st.session_state.continent = "Oceania"
    with col[0]:
        if st.button("North America", width=700):
            st.session_state.continent = "North America"
    with col[1]:
        if st.button("South America", width=700):
            st.session_state.continent = "South America"

    return st.session_state.continent



def country_filter(countries_list):
    col1, col2 = st.columns(2)
    with col1:
        country1 = st.selectbox(label="Filter by country", options=countries_list)
    with col2:
        country2 = st.selectbox(label="Select another country to compare", options=countries_list)

    selected_countries = []
    if country1 and country1 !="Alla":
        selected_countries.append(country1)
    if country2 and country2 !="Alla" and country2 != country1:
        selected_countries.append(country2)

    return selected_countries


def date_filter(date_list):
    #return st.selectbox(label="Filter by date", options=date_list)

    return st.select_slider(
        label="Filter by dates",
        options=date_list,
        value=(date_list[0], date_list[-1]))