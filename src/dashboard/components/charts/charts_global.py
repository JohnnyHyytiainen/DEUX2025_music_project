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


# Scatterplot (Punkt diagram där X-axis är danceability och Y-axis är Energy)
def create_dancefloor_scatter(df):
    """Creates a scatter plot for Energy VS Danceability on SONG level."""
    fig = px.scatter(
        df,
        x="Danceability",
        y="Energy",
        hover_name="Song",
        hover_data=["Artist"],
        color="Energy",
        color_continuous_scale="Plasma",
        labels={
            "Danceability": "Danceability Index (0-100)",
            "Energy": "Energy Index (0-100)",
        },
        title="The Global Dancefloor: Energy vs. Danceability",
    )
    fig.update_layout(coloraxis_showscale=False)
    # Lägg till ett kors i mitten som referens (index 50)
    fig.add_vline(x=50, line_dash="dash", line_color="#8D8D8D", opacity=0.65)
    fig.add_hline(y=50, line_dash="dash", line_color="#8D8D8D", opacity=0.5)

    # Tvinga axlarna att visa hela spannet så man ser tomrummen
    fig.update_xaxes(range=[0, 100])
    fig.update_yaxes(range=[0, 100])
    return fig


# Hbar chart, liggande stapeldiagram över aucustic countries.
def create_acoustic_bar_chart(df, is_acoustic=True):
    """Creates a horizontal barchart over the most aucustic Nations"""
    color = "#2E8B57" if is_acoustic else "#8A2BE2"
    order = "total ascending" if is_acoustic else "total descending"

    fig = px.bar(
        df,
        x="avg_acousticness",
        y="country",
        orientation="h",
        color_discrete_sequence=[color],
        labels={"country": "", "avg_acousticness": "Acousticness Index (0-100)"},
    )
    fig.update_layout(yaxis={"categoryorder": order})
    return fig
