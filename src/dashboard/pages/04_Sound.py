import streamlit as st
from components.data_loader import fetch_data
from components.queries.queries_physical_media import get_media_sales_query
from components.charts.charts_sound import top_country_profile_chart, top_songs_profile_list
from components.filter.filter_sound import procent_slider, vertical_procent_slider, vertical_bpm_slider, vertical_loudness_slider, explicit_chooser, mode_chooser

st.set_page_config(page_title="Sounds", page_icon="🎶", layout="wide")

best_match = st.container()

st.write("---")

col_table, col_controls, col_chart = st.columns([3, 3, 3])


with col_controls:
    st.subheader("Filter by audio features",text_alignment="center")
    row1_col1, row1_col2, row1_col3 = st.columns(3,width=300)
    with row1_col1:
        tempo_slider = vertical_bpm_slider(name="Tempo (BPM)")
    with row1_col2:
        loudness_slider = vertical_loudness_slider(name="Loudness (dBFS)")
    with row1_col3:
        liveness_slider = vertical_procent_slider(name="Liveness %")
    
    st.write("")
    row2_col1, row2_col2, row2_col3 = st.columns(3,width=300)
    with row2_col1:
        danceability_slider = vertical_procent_slider(name="Danceability %")
    with row2_col2:
        happiness_slider = vertical_procent_slider(name="Happiness %")
    with row2_col3:
        speechiness_slider = vertical_procent_slider(name="Speechiness %")
    
    st.write("")
    row3_col1, row3_col2 = st.columns(2)
    with row3_col1:
        is_explicit = explicit_chooser()
    with row3_col2:
        is_mode = mode_chooser()

    
with col_chart:
    top_country_profile_chart(
        tempo_max=tempo_slider,
        loudness_max=loudness_slider,
        liveness_max=liveness_slider,
        danceability_max=danceability_slider,
        happiness_max=happiness_slider,
        speechiness_max=speechiness_slider,
        explicit=is_explicit,
        mode=is_mode
    )

with col_table:
    df_returned = top_songs_profile_list(
        tempo_max=tempo_slider,
        loudness_max=loudness_slider,
        liveness_max=liveness_slider,
        danceability_max=danceability_slider,
        happiness_max=happiness_slider,
        speechiness_max=speechiness_slider,
        explicit=is_explicit,
        mode=is_mode
    )

with best_match:
    if df_returned is not None and not df_returned.empty:
        best_song = df_returned.iloc[0]["Song"]
        best_artist = df_returned.iloc[0]["Artist"]
        st.subheader("Best match")
        with st.container(border=True):
            st.metric(label=best_artist, value=best_song)
