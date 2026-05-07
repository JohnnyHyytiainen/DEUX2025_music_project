import streamlit as st
from components.data_loader import fetch_data
from components.queries.queries_global import get_continent_list_query
from components.queries.queries_streams import get_countries_list_query, get_date_list_query, table_query
from components.filter.filters_streams import continent_filter, country_filter, date_filter, reset_filters_streams,format_streams_table
from components.charts.charts_streams import streams_over_time_line_chart

st.markdown("""
    <style>
    .stButton button[kind="primary"] {
        background-color: #4CAF50 !important;
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# read css-file
# with open("style.css") as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# create column for reset button
r_col1, r_col2 = st.columns([18, 1])

# collect data for continents and dates
df_cont = fetch_data(get_continent_list_query())
continents = ["All"] + df_cont["continent"].tolist()

df_dates = fetch_data(get_date_list_query())
dates = df_dates["snapshot_date"].tolist()

# add reset button in column
with r_col2:
    reset_filters_streams(dates)


# create columns for toplist and filters
col1, col2, col3 = st.columns([5, 1, 8])

# add filters to the page in column 3
with col3:
    with st.container(border=True):
        st.markdown("###### Filter by continent")
        selected_cont = continent_filter(continents)


        df_country = fetch_data(get_countries_list_query(selected_cont))
        countries = ["All"] + df_country["country"].tolist()
        selected_countries = country_filter(countries)

        if "selected_dates" not in st.session_state:
            st.session_state.selected_dates = (dates[0], dates[-1])

        start_date, end_date = date_filter(dates)

# add table to page in column one
with col1:
    st.markdown("### Top 5 most streamed")

    df = fetch_data(table_query(selected_cont, selected_countries, start_date, end_date))
    df.index = df.index + 1
    df['Streams'] = df['Streams'].apply(format_streams_table)

    # set width to columns in table
    st.dataframe(df,
                 column_config={df.columns[0]: st.column_config.Column(width=140),
                                df.columns[1]: st.column_config.Column(width=140),}
                 )

# add line chart
st.plotly_chart(streams_over_time_line_chart(selected_cont, selected_countries, start_date, end_date))

