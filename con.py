# streamlit_app.py

import streamlit as st
import mysql.connector
import pandas as pd
def app():
    # Initialize connection.
    # Uses st.cache to only run once.
    @st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
    def init_connection():
        return mysql.connector.connect(**st.secrets["mysql"])

    conn = init_connection()

    # Perform query.
    # Uses st.cache to only rerun when the query changes or after 10 min.
    @st.cache(ttl=600)
    def run_query(query):
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    rows = run_query("SELECT * from Dataframe;")
    cases = run_query("SELECT date , cases from Dataframe;")
    deaths = run_query("SELECT date , deaths from Dataframe;")
    cases_df = pd.DataFrame(cases)
    deaths_df = pd.DataFrame(deaths)
    cases_df = cases_df.set_axis(['day',  'cases'], axis=1, inplace=False)
    deaths_df = deaths_df.set_axis(['day', 'deaths'], axis=1, inplace=False)


    df = pd.DataFrame(rows)
    df = df.set_axis(['day', 'deaths', 'cases'], axis=1, inplace=False)
    st.write(cases_df)
    st.write(df)

    # Print results.
#     for row in rows:
#         st.write(f"{row[0]} has a :{row[1]}:")
