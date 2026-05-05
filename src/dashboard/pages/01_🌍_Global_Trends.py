# 01_🌍_Global_Trends.py
# Kommentarer: Svenska
# Kod: Engelska
import streamlit as st
from components.data_loader import fetch_data
from components.queries.queries_global import (
    get_top_explicit_query,
    get_continent_list_query,
    get_mood_and_tempo_query,
    get_dj_crate_query,
    get_dancefloor_songs_query,
    get_acoustic_loudness_query,
)
from components.charts.charts_global import (
    create_explicit_bar_chart,
    create_mood_bar_chart,
    create_tempo_bar_chart,
    create_dancefloor_scatter,
    create_acoustic_bar_chart,
)

st.set_page_config(page_title="Global Music Trends", page_icon="🌍", layout="wide")


# ==========================================
# 1) STREAMLIT STATE MANAGEMENT & HELPERS
# ==========================================
def initialize_state():
    """Initiates all needed session_states dynamically."""
    state_keys = ["explicit_continent", "mood_continent", "anatomy_continent"]
    for keys in state_keys:
        if keys not in st.session_state:
            st.session_state[keys] = "Global"


# ---- reset för region filter -----
def reset_all_filters():
    """Resets all Continent/region filters to its Global State"""
    st.session_state.explicit_continent = "Global"
    st.session_state.mood_continent = "Global"
    st.session_state.anatomy_continent = "Global"


# ---- Privat helper funktion för mina columner vid jämförelser top10/bottom10 ----
def _render_comparison_columns(
    df, sort_col: str, title_top: str, title_bottom: str, chart_func
):
    """DRY helper to render TOP 10 columns vs BOTTOM 10 columns side by side."""
    col1, col2 = st.columns(2)
    top_df = df.sort_values(by=sort_col, ascending=False).head(10)
    bottom_df = df.sort_values(by=sort_col, ascending=True).head(10)

    with col1:
        st.markdown(f"**{title_top}**")
        # chart_func tar emot DataFrame och True för den "positiva/övre" egenskapen den ska ha
        st.plotly_chart(chart_func(top_df, True), use_container_width=True)

    with col2:
        st.markdown(f"**{title_bottom}**")
        # chart_func tar emot DataFrame och False för den "Negativa/undre" egenskapen den ska ha
        st.plotly_chart(chart_func(bottom_df, False), use_container_width=True)


# ====================================================================
# 2) UI SECTIONS - ENCAPSULATION
# ====================================================================
# Explicit query + bar-chart
def render_explicit_section(continent_list):
    st.subheader("Explicit Music")
    selected_explicit = st.selectbox(
        "Select Region for Explicit Music:",
        options=continent_list,
        key="explicit_continent",
    )
    df_explicit = fetch_data(get_top_explicit_query(selected_explicit))

    if not df_explicit.empty:
        st.plotly_chart(
            create_explicit_bar_chart(df_explicit), use_container_width=True
        )


# Mood and Tempo query + mood char-chart
def render_mood_and_tempo_section(continent_list):
    st.subheader("Cultural Differences: Happiness & Tempo")
    selected_mood = st.selectbox(
        "Select Region for Mood & Tempo:", options=continent_list, key="mood_continent"
    )
    df_mood = fetch_data(get_mood_and_tempo_query(selected_mood))

    if not df_mood.empty:
        tab_happy, tab_tempo = st.tabs(["Happiness (Valence)", "Tempo (BPM)"])

        with tab_happy:
            _render_comparison_columns(
                df=df_mood,
                sort_col="happiness_score",
                title_top=f"The Happiest Nations in the Region ({selected_mood})",
                title_bottom=f"The Most Melancholic Nations in the Region ({selected_mood})",
                chart_func=create_mood_bar_chart,
            )

        with tab_tempo:
            _render_comparison_columns(
                df=df_mood,
                sort_col="avg_bpm",
                title_top=f"Fastest Tempo in the Region ({selected_mood})",
                title_bottom=f"Slowest Tempo in the Region ({selected_mood})",
                chart_func=create_tempo_bar_chart,
            )


# Music anatomy (Aucustic vs Produced music) query + bar-chart
# + scatter plot over nations
def render_anatomy_section(continent_list):
    st.subheader("Deep Dive into Musical Anatomy")
    selected_anatomy = st.selectbox(
        "Select region for Musical Anatomy",
        options=continent_list,
        key="anatomy_continent",
    )
    df_dance = fetch_data(get_dancefloor_songs_query(selected_anatomy))
    df_acoustic = fetch_data(get_acoustic_loudness_query(selected_anatomy))

    if not df_dance.empty and not df_acoustic.empty:
        tab_dance, tab_acoustic = st.tabs(
            ["The Global Dancefloor", "Acoustic Vs Produced"]
        )

        with tab_dance:
            st.markdown("**Does High energy equal danceable music?**")
            st.write(
                "The dots show the average per Country. The lines are the Global average."
            )
            st.plotly_chart(
                create_dancefloor_scatter(df_dance), use_container_width=True
            )

        with tab_acoustic:
            st.markdown("**The Acoustic sound VS The Electronic sound**")
            st.write(
                "Compare the nations that love Acustic instruments with those that prefer heavily produced electronic beats."
            )
            _render_comparison_columns(
                df=df_acoustic,
                sort_col="avg_acousticness",
                title_top="The Acoustic Lounge",
                title_bottom="The Electronic Club",
                chart_func=create_acoustic_bar_chart,
            )


# Songfinder ifrån PowerBI dashboarden.
def render_dj_matcher_section():
    st.header("DJ Music Matcher")
    st.markdown(
        "Find the perfect songs for your playlist based on technical parameters."
    )

    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3)
    with ctrl_col1:
        bpm_range = st.slider("Select BPM range:", 60, 200, (60, 200))
        is_explicit = st.checkbox("Show only Explicit songs", value=False)
    with ctrl_col2:
        valence_range = st.slider("Happiness (Valence %):", 0, 100, (0, 100))
        limit_top = st.checkbox("Show only Top 20", value=True)
    with ctrl_col3:
        energy_range = st.slider("Energy level (Energy %):", 0, 100, (0, 100))

    query_dj = get_dj_crate_query(
        bpm_range, valence_range, energy_range, is_explicit, limit_top
    )
    df_dj = fetch_data(query_dj)

    if not df_dj.empty:
        st.success(f"Found {len(df_dj)} songs that match your criteria!")
        st.dataframe(df_dj, use_container_width=True, hide_index=True)
    else:
        st.warning("No songs matched that combination. Try expanding your search!")


# ====================================================
# 3) MAIN CONTROLLER funktion (Dirigenten för allting)
# ====================================================
def main():
    initialize_state()

    # Header
    st.title("Cultural Differences in Music")
    st.markdown("Explore how different regions consume music based on Spotify's data.")
    st.button("Reset ALL Region Filters", on_click=reset_all_filters, type="primary")
    st.divider()

    # Global Data Fetcher
    df_continents = fetch_data(get_continent_list_query())
    continent_list = (
        ["Global"] + df_continents["continent"].tolist()
        if not df_continents.empty
        else ["Global"]
    )

    # Render Sections och sätt dividers mellan varje section
    render_explicit_section(continent_list)
    st.divider()

    render_mood_and_tempo_section(continent_list)
    st.divider()

    render_anatomy_section(continent_list)
    st.divider()

    render_dj_matcher_section()


# ===============================================
# 3) MAIN controller funktionen för varje sektion
# ===============================================
def main():
    initialize_state()

    # Header
    st.title("Cultural Differences in Music")
    st.markdown("Explore how different regions consume music based on Spotify's data.")
    st.button("Reset ALL Region Filters", on_click=reset_all_filters, type="primary")
    st.divider()

    # Global Data Fetch
    df_continents = fetch_data(get_continent_list_query())
    continent_list = (
        ["Global"] + df_continents["continent"].tolist()
        if not df_continents.empty
        else ["Global"]
    )

    # Render Sections
    render_explicit_section(continent_list)
    st.divider()

    render_mood_and_tempo_section(continent_list)
    st.divider()

    render_anatomy_section(continent_list)
    st.divider()

    render_dj_matcher_section()


if __name__ == "__main__":
    main()
