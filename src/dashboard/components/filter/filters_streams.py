import streamlit as st


def continent_filter(continents):
    if "continent" not in st.session_state:
        st.session_state.continent = "Alla"

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


# def date_filter(date_list):
#     if "selected_dates" not in st.session_state:
#         st.session_state.selected_dates = (date_list[0], date_list[-1])
#
#     current_value = st.session_state.selected_dates
#
#     new_value  = st.select_slider(
#         label="Filter by dates",
#         options=date_list,
#         value=st.session_state.selected_dates
#     )
#
#     if new_value != current_value:
#         st.session_state.selected_dates = new_value
#
#     return st.session_state.selected_dates

def date_filter(date_list):
    # Skapa en unik key baserat på reset_counter
    if "reset_counter" not in st.session_state:
        st.session_state.reset_counter = 0

    key = f"date_slider_{st.session_state.reset_counter}"

    return st.select_slider(
        label="Filter by dates",
        options=date_list,
        value=(date_list[0], date_list[-1]),
        key=key  # ← ny key varje gång reset trycks
    )

def reset_filters_streams(date_list):
    if st.button("Reset", width=200):
        st.session_state.continent = "Alla"
        st.session_state.selected_countries = []
        if "reset_counter" not in st.session_state:
            st.session_state.reset_counter = 0
        st.session_state.reset_counter += 1  # ← ändrar key varje gång
        st.rerun()


def format_streams_table(number):
    if number >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number/1_000:.1f}K"
    else:
        return str(int(number))