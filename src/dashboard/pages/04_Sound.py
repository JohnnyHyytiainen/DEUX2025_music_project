import streamlit as st
from components.data_loader import fetch_data
from components.queries.queries_physical_media import get_media_sales_query
from components.charts.charts_sound import top_country_profile_chart, top_songs_profile_list, spotify_button
from components.filter.filter_sound import procent_slider, vertical_procent_slider, vertical_bpm_slider, vertical_loudness_slider, explicit_chooser, mode_chooser

st.set_page_config(page_title="Sounds", page_icon="🎶", layout="wide")

# AREA 1 - TITLE
# ToDo - Add a Title

# AREA 2 - MIDDLE

# 10 TOP SONGS + FILTERS & BEST MATCH 
area2_col1, area2_col2 = st.columns([30, 70])

with area2_col2:
    # BEST MATCH + SPOTIFY LINK (PLACEHOLDERS)
    area2_col2_row1_obj1, area2_col2_row1_obj2 = st.columns([70, 30],vertical_alignment="top")
    st.subheader("Filter by audio features",text_alignment="center")

    #SLIDERS
    area2_col2_row2_start, area2_col2_row2_obj1, area2_col2_row2_obj2, area2_col2_row2_obj3, area2_col2_row2_obj4, area2_col2_row2_obj5, area2_col2_row2_obj6, area2_col2_row2_end = st.columns([1, 2, 2, 2, 2, 2, 2, 1])
    with area2_col2_row2_obj1:
        tempo_slider = vertical_bpm_slider(name="Tempo (BPM)")
    with area2_col2_row2_obj2:
        loudness_slider = vertical_loudness_slider(name="Loudness (dBFS)")
    with area2_col2_row2_obj3:
        liveness_slider = vertical_procent_slider(name="Liveness %")
    with area2_col2_row2_obj4:
        danceability_slider = vertical_procent_slider(name="Danceability %")
    with area2_col2_row2_obj5:
        happiness_slider = vertical_procent_slider(name="Happiness %")
    with area2_col2_row2_obj6:
        speechiness_slider = vertical_procent_slider(name="Speechiness %")

    # SWITCHES
    area2_col2_row3_start, area2_col2_row3_obj1, area2_col2_row3_obj2, area2_col2_row3_end = st.columns([1, 2, 2, 1])
    with area2_col2_row3_obj1:
        is_explicit = explicit_chooser()
    with area2_col2_row3_obj2:
        is_mode = mode_chooser()


# 10 TOP SONGS
with area2_col1:
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

# BEST MATCH & SPOTIFY LINK
if df_returned is not None and not df_returned.empty:
    best_song = df_returned.iloc[0]["Song"]
    best_artist = df_returned.iloc[0]["Artist"]
    best_id = df_returned.iloc[0]["Spotify_ID"]
    
    # BEST MATCH
    with area2_col2_row1_obj1:
        with st.container(border=True):
            st.metric(label=best_artist, value=best_song)

    with area2_col2_row1_obj2:
        spotify_button(best_id)

# AREA 3 - CHART
area3_col1 = st.container()

with area3_col1:
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