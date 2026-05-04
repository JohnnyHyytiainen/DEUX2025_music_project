import streamlit as st
from components.data_loader import fetch_data

df_top_country_profile = fetch_data("""
        SELECT
            d.country_name as country,
            COUNT(DISTINCT s.name) as songs
        FROM silver_spotify_daily s
        INNER JOIN dim_geography d ON s.country = d.iso_code
        WHERE
            energy BETWEEN 0.2 AND 0.8 AND
            speechiness BETWEEN 0.2 AND 0.8 AND
            valence BETWEEN 0.2 AND 0.8 AND
            liveness BETWEEN 0.2 AND 0.8 AND
            danceability BETWEEN 0.2 AND 0.8 AND
            tempo BETWEEN 100 AND 200 AND  
            loudness BETWEEN -50 AND 0 AND
            is_explicit = 1 AND
            "mode" = 0             
        GROUP BY country_name
        ORDER BY songs DESC;
    """)

def top_country_profile_chart(number_countries=5):
    with st.container(border=True):
        st.markdown("**Top Counties to your profile**")
        st.bar_chart(
            df_top_country_profile.head(number_countries),
            x="country",
            y="songs",
            x_label="COUNTRIES",
            y_label="NR SONGS",
        )