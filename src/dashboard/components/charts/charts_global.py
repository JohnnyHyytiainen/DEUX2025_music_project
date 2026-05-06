import plotly.express as px
import pandas as pd


# ==============================================================
# SPEKTRUM-GRAFER FÖR MOOD OCH TEMPO (MAKRO-PERSPEKTIV)
# ==============================================================


def create_mood_spectrum_chart(df):
    """Creates a single macro-level bar chart for Happiness with a color gradient."""
    # Sortera så att det gladaste landet hamnar högst upp i grafen
    df_sorted = df.sort_values(by="happiness_score", ascending=True)

    fig = px.bar(
        df_sorted,
        x="happiness_score",
        y="country",
        orientation="h",
        color="happiness_score",
        color_continuous_scale=["#1A1A95", "#CBC835"],
        labels={"country": "", "happiness_score": "Happiness Index (0-100)"},
    )

    fig.update_layout(
        coloraxis_showscale=False,
        xaxis=dict(range=[0, 100]),  # TVINGA axeln till 0-100 enligt UX-krav
        plot_bgcolor="rgba(0,0,0,0.08)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),  # Minskar onödiga marginaler
    )
    return fig


def create_acoustic_spectrum_chart(df):
    """Creates a macro-level bar chart for Acousticness vs Electronic."""
    df_sorted = df.sort_values(by="avg_acousticness", ascending=True)

    fig = px.bar(
        df_sorted,
        x="avg_acousticness",
        y="country",
        orientation="h",
        color="avg_acousticness",
        color_continuous_scale=[
            "#8A2BE2",
            "#2E8B57",
        ],
        labels={"country": "", "avg_acousticness": "Acousticness Index (0-100)"},
    )

    fig.update_layout(
        coloraxis_showscale=False,
        xaxis=dict(range=[0, 100]),
        plot_bgcolor="rgba(0,0,0,0.08)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
    )
    return fig


def create_explicit_spectrum_chart(df):
    """Creates a macro-level bar chart for share of Explicit music."""
    df_sorted = df.sort_values(by="Explicit_Procent", ascending=True)

    fig = px.bar(
        df_sorted,
        x="Explicit_Procent",
        y="country",
        orientation="h",
        color="Explicit_Procent",
        color_continuous_scale="Purples",
        labels={"country": "", "Explicit_Procent": "Explicit Music (%)"},
    )

    fig.update_layout(
        coloraxis_showscale=False,
        xaxis=dict(range=[0, 100]),
        plot_bgcolor="rgba(0,0,0,0.08)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
    )
    return fig


def create_tempo_spectrum_chart(df):
    """Creates a single macro-level bar chart for Tempo with a color gradient."""
    df_sorted = df.sort_values(by="avg_bpm", ascending=True)

    fig = px.bar(
        df_sorted,
        x="avg_bpm",
        y="country",
        orientation="h",
        color="avg_bpm",
        color_continuous_scale=["#4B4BFF", "#FF4B4B"],
        labels={"country": "", "avg_bpm": "Average Tempo (BPM)"},
    )

    fig.update_layout(
        coloraxis_showscale=False,
        xaxis=dict(range=[60, 160]),
        plot_bgcolor="rgba(0,0,0,0.08)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
    )
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
    fig.add_vline(x=50, line_dash="dash", line_color="#8D8D8D", opacity=0.60)
    fig.add_hline(y=50, line_dash="dash", line_color="#8D8D8D", opacity=0.60)

    # --- UX COPY, TEXT I FYRA HÖRNEN ---
    fig.add_annotation(
        x=5, y=95, text="High Energy<br>Low Danceability", showarrow=False, opacity=0.8
    )
    fig.add_annotation(
        x=95,
        y=95,
        text="High Energy<br>High Danceability",
        showarrow=False,
        opacity=0.8,
    )
    fig.add_annotation(
        x=5, y=5, text="Low Energy<br>Low Danceability", showarrow=False, opacity=0.8
    )
    fig.add_annotation(
        x=95, y=5, text="Low Energy<br>High Danceability", showarrow=False, opacity=0.8
    )
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
