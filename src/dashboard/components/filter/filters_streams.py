import streamlit as st


def continent_filter(continents_list):
    return st.selectbox(label="Filter by continent", options=continents_list)


def country_filter(countries_list):
    return st.selectbox(label="Filter by country", options=countries_list)


def date_filter(date_list):
    return st.selectbox(label="Filter by date", options=date_list)
    # implement slider as well?