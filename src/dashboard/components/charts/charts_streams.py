import plotly.express as px
from components.data_loader import fetch_data
from components.queries.queries_streams import line_chart_query

#create colors for lines in linechart
country_lines_color=[
    "#CE917A",
    "#77989C"
]


def streams_over_time_line_chart(selected_cont, selected_countries, start_date, end_date):
    """Create a linechart to show streams over time in different countries"""
    df = fetch_data(line_chart_query(selected_cont, selected_countries, start_date, end_date))

    if "Country" in df.columns: # one or two countries selected -> one colored line per country
        fig = px.line(
            df,
            x="Date",
            y="Amount of streams",
            color="Country",
            color_discrete_sequence=country_lines_color # getting chosen colors
        )
    # no country selected -> one line showing total streams combining all countries
    else:
        fig = px.line(
            df,
            x="Date",
            y="Amount of streams",
            color_discrete_sequence=country_lines_color
        )

    # Adjust the title of the chart
    fig.update_layout(
        title=dict(text="Total number of streams over time", font=dict(size=26), automargin=True, yref='paper', x=0.02),
    )
    fig.update_yaxes(
        showgrid=True,
        griddash='dot',
        layer='below traces',
        gridcolor='#AAAAAA'
    )

    return fig





