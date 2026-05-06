import plotly.express as px
import pandas as pd


# ===========================================
# BASE CHART BUILDER PRIV FUNKTION DONT TOUCH
# ===========================================
def _create_base_hbar_chart(
    df, x_col: str, x_label: str, color: str, is_ascending: bool
):
    """Base function to generate horizontal bar-charts with consistent styling"""
    order = "total ascending" if is_ascending else "total descending"

    fig = px.bar(
        df,
        x=x_col,
        y="country",
        orientation="h",
        color_discrete_sequence=[color],
        labels={"country": "", x_col: x_label},
    )
    fig.update_layout(yaxis={"categoryorder": order})
    return fig


# ---------- SPECIFIKA CHARTS MED BASE CHART BUILDER ----------
# Mood H bar-chart
def create_mood_bar_chart(df, is_happy=True):
    """Creates horizontal bar chart for happy and melancholic music."""
    color = "#CBC835" if is_happy else "#1A1A95"
    return _create_base_hbar_chart(
        df=df,
        x_col="happiness_score",
        x_label="Happiness Index (0-100)",
        color=color,
        is_ascending=is_happy,
    )


# ---------- SPECIFIKA CHARTS MED BASE CHART BUILDER ----------
# Tempo H bar-chart vid sidan av mood chart
def create_tempo_bar_chart(df, is_fast=True):
    """Creates a H-bar chart for fast/slow tempo music."""
    color = "#CBC835" if is_fast else "#1A1A95"
    return _create_base_hbar_chart(
        df=df,
        x_col="avg_bpm",
        x_label="Average Tempo (BPM)",
        color=color,
        is_ascending=is_fast,
    )


# ---------- SPECIFIKA CHARTS MED BASE CHART BUILDER ----------
# Akustisk/producerad H bar-chart
# Grön "jordig ton" = akustisk musik.
# Lila "intensiv/artificiell ton" = producerad/elektronisk musik.
def create_acoustic_bar_chart(df, is_acoustic=True):
    """Creates a horizontal barchart over the most aucustic Nations"""
    color = "#2E8B57" if is_acoustic else "#8A2BE2"
    return _create_base_hbar_chart(
        df=df,
        x_col="avg_acousticness",
        x_label="Acousticness Index (0-100)",
        color=color,
        is_ascending=is_acoustic,
    )


# ===============================================================
# Skapar barchart för explicit musik och dess andel(%) för länder
# ===============================================================
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


# ============================================================
# Scatterplot där X-axis är danceability och Y-axis är Energy
# ============================================================
def create_dancefloor_scatter(df):
    """Creates a scatter plot for Energy VS Danceability on SONG level."""
    fig = px.scatter(
        df,
        x="Danceability",
        y="Energy",
        hover_name="Song",
        hover_data=["Artist"],
        color="Energy",
        color_continuous_scale="Burgyl",
        labels={
            "Danceability": "Danceability Index (0-100)",
            "Energy": "Energy Index (0-100)",
        },
        title="The Global Dancefloor: Energy vs. Danceability",
    )
    fig.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0, 0, 0, 0.03)",  # <-- Skapar en svag mörk, semi-transparent ruta
        paper_bgcolor="rgba(0, 0, 0, 0)",  # <-- Håller ytan runt grafen helt transparent
    )
    # Lägg till ett kors i mitten som referens (index 50)
    fig.add_vline(x=50, line_dash="dash", line_color="#8D8D8D", opacity=0.70)
    fig.add_hline(y=50, line_dash="dash", line_color="#8D8D8D", opacity=0.70)

    # Tvinga axlarna att visa hela spannet så man ser tomrummen
    fig.update_xaxes(range=[0, 100])
    fig.update_yaxes(range=[0, 100])
    return fig


# ===============================================================
# Radar chart för Kulturella jämförelser i regionens vibes/musik
# ===============================================================
def create_audio_signature_radar(df):
    """Creates a Radar chart comparing the audio DNA of two selected regions."""
    features = ["Danceability", "Energy", "Happiness", "Acousticness", "Speechiness"]

    # Smält datan från wide till long format
    df_melted = df.melt(
        id_vars=["Region"], value_vars=features, var_name="Feature", value_name="Score"
    )

    df_melted["Score"] = df_melted["Score"].round(1)

    # Spotify-grön och en snygg lila färg
    colors = ["#1DB954", "#8A2BE2"]

    fig = px.line_polar(
        df_melted,
        r="Score",
        theta="Feature",
        color="Region",
        line_close=True,
        color_discrete_sequence=colors,
        hover_name="Region",  # Sätter regionens namn i toppen av rutan jag hovrar över
        markers=True,
    )
    # %{theta} hämtar Feature (typ Energy) och %{r} hämtar Score.
    # <extra></extra> tar bort den extra fula rutan bredvid
    fig.update_traces(
        fill="toself",
        opacity=0.5,
        marker=dict(size=8),
        hovertemplate="<b>%{hovertext}</b><br>%{theta}: %{r}<extra></extra>",
    )

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0.03)",
            radialaxis=dict(
                visible=True,
                showticklabels=False,  # Gömmer statiska siffror, behöver ej det då jag kör hover over
                showgrid=True,
                gridcolor="rgba(0,0,0,0.03)",
                linecolor="rgba(0,0,0,0.03)",
            ),
            angularaxis=dict(
                gridcolor="rgba(0,0,0,0.03)", linecolor="rgba(0,0,0,0.03)"
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        title="Audio Signature (DNA)",
        hovermode="closest",
    )
    return fig
