# src/dashboard/pages/01_Global_Trends.py
import streamlit as st
from components.data_loader import fetch_data
from utils.helpers import (
    initialize_global_state,
    render_local_controls,
)

from components.queries.queries_global import (
    get_top_explicit_query,
    get_continent_list_query,
    get_countries_in_continent_query,
    get_mood_and_tempo_query,
    get_country_audio_signature_query,
    get_dancefloor_songs_query,
    get_acoustic_loudness_query,
)
from components.charts.charts_global import (
    create_explicit_spectrum_chart,
    create_mood_spectrum_chart,
    create_tempo_spectrum_chart,
    create_audio_signature_radar,
    create_dancefloor_scatter,
    create_acoustic_spectrum_chart,
)

st.set_page_config(page_title="Global Music Trends", page_icon="🌍", layout="wide")


# ===========
# UI SECTIONS
# ===========
def render_audio_signature_section(continent_list):
    st.header("The Cultural Audio Signature")
    current_cont, is_explicit = render_local_controls("audio_sig", continent_list)
    st.markdown(f"Compare the musical DNA of two countries within **{current_cont}**.")

    df_countries = fetch_data(get_countries_in_continent_query(current_cont))
    if df_countries.empty:
        st.warning("No countries found for this selection.")
        return

    country_list = df_countries["country_name"].tolist()

    col1, col2 = st.columns(2)
    with col1:
        c1 = st.selectbox(
            "Select Country 1:", options=country_list, index=0, key="sig_c1"
        )
    with col2:
        c2_index = 1 if len(country_list) > 1 else 0
        c2 = st.selectbox(
            "Select Country 2:", options=country_list, index=c2_index, key="sig_c2"
        )

    df_signature = fetch_data(get_country_audio_signature_query(c1, c2, is_explicit))

    if not df_signature.empty:
        col_text, col_chart = st.columns([1, 2.5])
        with col_text:
            st.write(f"**Comparing:**\n1. {c1}\n2. {c2}")
            st.write("Hover over the edges to see the exact scores.")
        with col_chart:
            st.plotly_chart(
                create_audio_signature_radar(df_signature), use_container_width=True
            )


def render_mood_and_tempo_section(continent_list):
    st.header("The Emotional Spectrum of Music")
    st.markdown(
        "A macro perspective on the emotional resonance and pace of the Music we listen to."
    )

    current_cont, is_explicit = render_local_controls("mood_section", continent_list)
    df_mood = fetch_data(get_mood_and_tempo_query(current_cont, is_explicit))

    if not df_mood.empty:
        tab_happy, tab_tempo = st.tabs(["Happiness (Valence)", "Tempo (BPM)"])

        with tab_happy:
            col_chart, col_notes = st.columns([3, 1])
            with col_chart:
                st.plotly_chart(
                    create_mood_spectrum_chart(df_mood), use_container_width=True
                )
            with col_notes:
                happiest_idx = df_mood["happiness_score"].idxmax()
                saddest_idx = df_mood["happiness_score"].idxmin()
                st.info(
                    "**What is Happiness (Valence)?**\nA measure from 0 to 100 describing the musical positiveness conveyed by a track."
                )

                st.metric(
                    "Happiest Nation",
                    df_mood.loc[happiest_idx, "country"],
                    f"{df_mood.loc[happiest_idx, 'happiness_score']:.1f} Index",
                )
                st.metric(
                    "Most Melancholic",
                    df_mood.loc[saddest_idx, "country"],
                    f"{df_mood.loc[saddest_idx, 'happiness_score']:.1f} Index",
                    delta_color="inverse",
                )

        with tab_tempo:
            col_chart_t, col_notes_t = st.columns([3, 1])
            with col_chart_t:
                st.plotly_chart(
                    create_tempo_spectrum_chart(df_mood), use_container_width=True
                )
            with col_notes_t:
                fastest_idx = df_mood["avg_bpm"].idxmax()
                slowest_idx = df_mood["avg_bpm"].idxmin()
                st.info(
                    "**About Tempo (BPM)**\nThe overall estimated tempo of a track in beats per minute."
                )

                st.metric(
                    "Fastest Pace",
                    df_mood.loc[fastest_idx, "country"],
                    f"{df_mood.loc[fastest_idx, 'avg_bpm']:.1f} BPM",
                )
                st.metric(
                    "Slowest Pace",
                    df_mood.loc[slowest_idx, "country"],
                    f"{df_mood.loc[slowest_idx, 'avg_bpm']:.1f} BPM",
                    delta_color="inverse",
                )


def render_anatomy_section(continent_list):
    st.header("Deep Dive into Musical Anatomy")
    st.markdown(
        "Exploring the dancefloor vibes, acoustic properties, and cultural acceptance of explicit content."
    )

    current_cont, is_explicit = render_local_controls("anatomy_section", continent_list)

    tab_names = ["The Global Dancefloor", "Acoustic Vs Produced"]
    if is_explicit:
        tab_names.append("Explicitness (%)")

    tabs = st.tabs(tab_names)

    df_dance = fetch_data(get_dancefloor_songs_query(current_cont, is_explicit))
    with tabs[0]:
        st.markdown("**Does High energy equal danceable music?**")
        if not df_dance.empty:
            st.plotly_chart(
                create_dancefloor_scatter(df_dance), use_container_width=True
            )

    df_acoustic = fetch_data(get_acoustic_loudness_query(current_cont, is_explicit))
    with tabs[1]:
        if not df_acoustic.empty:
            col_chart, col_notes = st.columns([3, 1])
            with col_chart:
                st.plotly_chart(
                    create_acoustic_spectrum_chart(df_acoustic),
                    use_container_width=True,
                )
            with col_notes:
                acoustic_idx = df_acoustic["avg_acousticness"].idxmax()
                electronic_idx = df_acoustic["avg_acousticness"].idxmin()
                st.info("**Acoustic vs Electronic (0-100)**")
                st.metric(
                    "Most Acoustic",
                    df_acoustic.loc[acoustic_idx, "country"],
                    f"{df_acoustic.loc[acoustic_idx, 'avg_acousticness']:.1f}",
                )
                st.metric(
                    "Most Electronic",
                    df_acoustic.loc[electronic_idx, "country"],
                    f"{df_acoustic.loc[electronic_idx, 'avg_acousticness']:.1f}",
                    delta_color="inverse",
                )

    if is_explicit:
        with tabs[2]:
            df_explicit = fetch_data(get_top_explicit_query(current_cont))
            if not df_explicit.empty:
                col_chart_e, col_notes_e = st.columns([3, 1])
                with col_chart_e:
                    st.plotly_chart(
                        create_explicit_spectrum_chart(df_explicit),
                        use_container_width=True,
                    )
                with col_notes_e:
                    most_exp_idx = df_explicit["Explicit_Procent"].idxmax()
                    st.info("**Explicit Music Share**")
                    st.metric(
                        "Most Explicit",
                        df_explicit.loc[most_exp_idx, "country"],
                        f"{df_explicit.loc[most_exp_idx, 'Explicit_Procent']:.1f}%",
                    )


# ===============
# MAIN CONTROLLER
# ===============
def main():
    initialize_global_state()

    st.title("Cultural Differences in Music")
    st.markdown(
        "Explore how different regions consume music based on Spotify's data. **Spanning from 2023 to 2025.**"
    )
    st.divider()

    df_continents = fetch_data(get_continent_list_query())
    continent_list = (
        ["Global"] + df_continents["continent"].tolist()
        if not df_continents.empty
        else ["Global"]
    )

    render_audio_signature_section(continent_list)
    st.divider()
    render_mood_and_tempo_section(continent_list)
    st.divider()
    render_anatomy_section(continent_list)


if __name__ == "__main__":
    main()
