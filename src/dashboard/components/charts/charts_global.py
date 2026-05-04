import plotly.express as px

# Script för att separera charts ifrån /pages/01_Global_Trends.py scriptet


# Skapar barchart för explicit andel(%) explicit musik per land i silver_spotify_daily table
def create_explicit_bar_chart(df):
    """Creates bar chart for share of explicit music by country"""
    fig = px.bar(
        df,
        x="country",
        y="Explicit_Procent",
        color="Explicit_Procent",
        color_continuous_scale="Purples",
        labels={"country": "Land", "Explicit_Procent": "Explicit Musik (%)"},
        title="Explicit Musik (%)",
    )
    fig.update_layout(coloraxis_showscale=False)
    return fig


# Ett Horisontellt stapeldiagram för humör (Glädje vs melankoli)
def create_mood_bar_chart(df, is_happy=True):
    """Creates horizontal bar chart for happy and melancholic music."""
    color = "#0DBDBD" if is_happy else "#0B0B65"
    order = "total ascending" if is_happy else "total descending"

    fig = px.bar(
        df,
        x="happiness_score",
        y="country",
        orientation="h",
        color_discrete_sequence=[color],
        labels={"country": "", "happiness_score": "Happiness Index (0-100)"},
    )
    fig.update_layout(yaxis={"categoryorder": order})
    return fig


# Tempo barchart
def create_tempo_bar_chart(df, is_fast=True):
    """Creates a H-bar chart for fast/slow tempo music."""
    # Röd/Orange för snabbt, Blå/Lila för långsamt
    color = "#FF4B4B" if is_fast else "#4B4BFF"
    order = "total ascending" if is_fast else "total descending"

    fig = px.bar(
        df,
        x="avg_bpm",
        y="country",
        orientation="h",
        color_discrete_sequence=[color],
        labels={"country": "", "avg_bpm": "Snitt Tempo (BPM)"},
    )
    fig.update_layout(yaxis={"categoryorder": order})
    return fig


# Scatterplot (Punkt diagram där Xaxis är danceability och Y-axis är Energy)
def create_dancefloor_scatter(df):
    """Creates a scatter plot for Energy VS Danceability"""
    fig = px.scatter(
        df,
        x="avg_danceability",
        y="avg_energy",
        hover_name="country",
        color="avg_energy",
        color_continuous_scale="Viridis",
        labels={
            "avg_danceability": "Danceability Index (0-100)",
            "avg_energy": "Energy Index (0-100)",
        },
        title="The Global Dancefloor: Energy vs. Danceability",
    )
    fig.update_layout(coloraxis_showscale=False)
    # Lägger till linjer för referens, snittvärden
    fig.add_vline(
        x=df["avg_danceability"].mean(),
        line_dash="dash",
        line_color="gray",
        opacity=0.5,
    )
    fig.add_hline(
        y=df["avg_energy"].mean(), line_dash="dash", line_color="gray", opacity=0.45
    )
    return fig


# Hbar chart, liggande stapeldiagram över aucustic countries.
def create_acoustic_bar_chart(df):
    """Creates a horizontal barchart over the most aucustic Nations"""
    fig = px.bar(
        df.sort_values(by="avg_acousticness", ascending=True).tail(
            15
        ),  # som head men visar top 15
        x="avg_acousticness",
        y="country",
        orientation="h",
        color_discrete_sequence=["#1FC913"],
        labels={"country": "", "avg_acousticness": "Acousticness Index (0-100)"},
        title="Top 15 Countries that loves their Aucustic music",
    )
    return fig
