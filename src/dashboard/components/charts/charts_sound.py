import streamlit as st
from components.data_loader import fetch_data
from assets.style.py_style import style_toplist


def top_songs_profile_list(
        speechiness_max=80,
        danceability_max=80,
        liveness_max=80,
        happiness_max=80,
        tempo_max=180,
        loudness_max=0,
        explicit="NO",
        mode="Major",
        limit=10):        
    speechiness = speechiness_max/100
    danceability = danceability_max/100
    liveness = liveness_max/100
    happiness = happiness_max/100
    expl_var = 0
    mode_var = 0
    expl_var = 1 if explicit == "YES" else 0
    mode_var = 1 if mode == "Major" else 0
    df_top_songs_profile = fetch_data(f"""
        SELECT
            name AS Song,
            artists AS Artist,
            SUM(popularity) AS Popularity,
            spotify_id AS Spotify_ID
        FROM silver_spotify_daily
        WHERE
            speechiness < {speechiness} AND
            valence < {happiness} AND
            liveness < {liveness} AND
            danceability < {danceability} AND
            tempo < {tempo_max} AND  
            loudness < {loudness_max} AND
            is_explicit = {expl_var} AND
            "mode" = {mode_var}             
        GROUP BY name, artists, spotify_id
        ORDER BY Popularity DESC
        LIMIT {limit};
    """)
    with st.container(border=True):
        st.subheader("Top 10 best matched")
        if not df_top_songs_profile.empty:
            df_top_songs_profile.index = df_top_songs_profile.index + 1

            df_to_show = df_top_songs_profile.drop(columns=["Popularity", "Artist", "Spotify_ID"])

            st.table(df_to_show)
        else:
            st.info("No songs found matching this exact profile. Try loosening the filters!")
        return df_top_songs_profile


def top_country_profile_chart(
        speechiness_max=80,
        danceability_max=80,
        liveness_max=80,
        happiness_max=80,
        tempo_max=180,
        loudness_max=0,
        explicit="NO",
        mode="Major",
        limit=10):
    speechiness = speechiness_max/100
    danceability = danceability_max/100
    liveness = liveness_max/100
    happiness = happiness_max/100
    expl_var = 0
    mode_var = 0
    expl_var = 1 if explicit == "YES" else 0
    mode_var = 1 if mode == "Major" else 0
    df_top_country_profile = fetch_data(f"""
        SELECT
            d.country_name as country,
            COUNT(DISTINCT s.name) as songs
        FROM silver_spotify_daily s
        INNER JOIN dim_geography d ON s.country = d.iso_code
        WHERE
            speechiness < {speechiness} AND
            valence < {happiness} AND
            liveness < {liveness} AND
            danceability < {danceability} AND
            tempo < {tempo_max} AND  
            loudness < {loudness_max} AND
            is_explicit = {expl_var} AND
            "mode" = {mode_var}             
        GROUP BY country_name
        ORDER BY songs DESC
        LIMIT {limit};
    """)
    with st.container(border=True):
        st.subheader("Coutries matching your sound profile")
        st.bar_chart(
            df_top_country_profile,
            x="country",
            y="songs",
            x_label=None,
            y_label=None,
            sort="-songs",
            color="#B33A38"
        )

    return

def spotify_button(spotify_id):
        spotify_url = f"https://open.spotify.com/track/{spotify_id}"
        try:
            with open("assets/pictures/Spotifybutton.svg", "r", encoding="utf-8") as svg_file:
                svg_content = svg_file.read()


                st.markdown(
f"""
<div style="max-width: 150px; cursor: pointer;">
<a href="{spotify_url}" target="_blank">
{svg_content}
</a>
</div>
""",
                unsafe_allow_html=True
                )
        
        except FileNotFoundError:
            st.error("Kunde inte hitta bilden Spotifybutton.svg")