import streamlit as st


def continent_filter(continents):
    """Create buttons with filters for continents"""
    if "continent" not in st.session_state:
        st.session_state.continent = "All"

    col = st.columns(3)

    # if continent is chosen, button will get another color (to show what filter is shown)
    with col[2]:
        if st.session_state.continent == "Europe":
            st.button("Europe", width=700, type="primary")
        else:
            if st.button("Europe", width=700):
                st.session_state.continent = "Europe"
                st.rerun()
    with col[0]:
        if st.session_state.continent == "Asia":
            st.button("Asia", width=700, type="primary")
        else:
            if st.button("Asia", width=700):
                st.session_state.continent = "Asia"
                st.rerun()
    with col[1]:
        if st.session_state.continent == "Africa":
            st.button("Africa", width=700, type="primary")
        else:
            if st.button("Africa", width=700):
                st.session_state.continent = "Africa"
                st.rerun()
    with col[2]:
        if st.session_state.continent == "Oceania":
            st.button("Oceania", width=700, type="primary")
        else:
            if st.button("Oceania", width=700):
                st.session_state.continent = "Oceania"
                st.rerun()
    with col[0]:
        if st.session_state.continent == "North America":
            st.button("North America", width=700, type="primary")
        else:
            if st.button("North America", width=700):
                st.session_state.continent = "North America"
                st.rerun()
    with col[1]:
        if st.session_state.continent == "South America":
            st.button("South America", width=700, type="primary")
        else:
            if st.button("South America", width=700):
                st.session_state.continent = "South America"
                st.rerun()

    return st.session_state.continent


def country_filter(countries_list):
    """Create dropdowns to choose countries"""
    col1, col2 = st.columns(2)
    with col1:
        country1 = st.selectbox(label="Filter by country", options=countries_list)
    with col2:
        country2 = st.selectbox(label="Filter by second country to compare", options=countries_list)

    # create list of chosen countries, no chosen countries -> returns empty list
    selected_countries = []
    if country1 and country1 !="All":
        selected_countries.append(country1)
    if country2 and country2 !="All" and country2 != country1:
        selected_countries.append(country2)

    return selected_countries



def date_filter(date_list):
    """Create slider to choose inbetween dates"""
    if "reset_counter" not in st.session_state:
        st.session_state.reset_counter = 0

    # create unique key that changes on every reset (help from llm)
    key = f"date_slider_{st.session_state.reset_counter}"

    return st.select_slider(
        label="Filter by dates",
        options=date_list,
        value=(date_list[0], date_list[-1]),
        key=key
    )


def reset_filters_streams(date_list):
    """Create a button to reset filters"""
    if st.button("Reset", width=200):
        st.session_state.continent = "All"
        st.session_state.selected_countries = []

        # increase counter to create new key for date slider (help from llm)
        if "reset_counter" not in st.session_state:
            st.session_state.reset_counter = 0
        st.session_state.reset_counter += 1

        # force streamlit to reload the page
        st.rerun()


def format_streams_table(number):
    """Format streams table to M (million)"""
    if number >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number/1_000:.1f}K"
    else:
        return str(int(number))