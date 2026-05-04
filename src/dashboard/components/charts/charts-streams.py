import streamlit as st
import duckdb
#from ... import ...


df_streams_over_time = duckdb.sql("""-sql
    
    SELECT date and SUM of streams
    
""")


def streams_over_time_chart(number_countries=2):
    """Creante a linechart to show streams over time in different countries"""
    st.line_chart(
        # create line chart where xaxis is sum of streams and yaxis is date
        # show X countries/lines? check with UX (in charge of the graphics)
    )