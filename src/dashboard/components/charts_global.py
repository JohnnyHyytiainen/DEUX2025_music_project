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
        labels={"country": "", "happiness_score": "Glädje Index (0-100)"},
    )
    fig.update_layout(yaxis={"categoryorder": order})
    return fig


# Tempo linjediagram för BPM
def create_tempo_line_chart(df):
    """Creates a line chart for BPM(Beats Per Minute)"""
    fig = px.line(
        df,
        x="country",
        y="avg_bpm",
        markers=True,
        color_discrete_sequence=["#F5640A"],
        labels={"country": "Land", "avg_bpm": "Snitt Tempo (BPM)"},
    )
    fig.update_yaxes(range=[df["avg_bpm"].min() - 2, df["avg_bpm"].max() + 2])
    return fig


# Skapar stapeldiagram för kontinenter
def create_continent_bpm_chart(df):
    """Creates bar charts with some error margins for continents."""
    fig = px.bar(
        df,
        x="continent",
        y="Avg_BPM",
        range_y=[100, 140],
        color="Avg_BPM",
        color_continuous_scale="Reds",
        error_y=df["Max_BPM"] - df["Avg_BPM"],
        error_y_minus=df["Avg_BPM"] - df["Min_BPM"],
        labels={"continent": "Kontinent", "Avg_BPM": "Genomsnittligt BPM"},
        title="Genomsnittligt Tempo med Spridning (Min/Max)",
    )
    fig.update_layout(coloraxis_showscale=False)
    return fig
