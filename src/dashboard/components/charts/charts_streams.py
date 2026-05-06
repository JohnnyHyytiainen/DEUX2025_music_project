import plotly.express as px
from components.data_loader import fetch_data
from components.queries.queries_historical import line_chart_query



def streams_over_time_line_chart(selected_cont, selected_countries, start_date, end_date):
    """Creante a linechart to show streams over time in different countries"""
    df = fetch_data(line_chart_query(selected_cont, selected_countries, start_date, end_date))

    if "Country" in df.columns:
        fig = px.line(
            df,
            x="Date",
            y="Streams",
            color="Country",
        )
    else:
        fig = px.line(
            df,
            x="Date",
            y="Streams"
        )

    return fig





