import os.path

import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
url = "https://uzu34h3kfl.execute-api.eu-central-1.amazonaws.com/test/ov_fietsen"

def app():
    st.title('Verwachte OV fiets beschikbaarheid')
    path="/Users/eefje/python_projects/ovfiets/data/ovfietsen_2022-10-24.csv"
    gemeentes = pd.read_csv(path)
    gemeente_selecties = gemeentes.Station.unique().tolist()
    station = st.selectbox('Station', gemeente_selecties)

    datum = st.date_input(
        "Datum", datetime.today(), min_value=datetime.today(), max_value=datetime.today()+timedelta(days=14))
    datum = str(datum)

    tijd = st.time_input(
        "Tijd", datetime.now())
    tijd = str(tijd)


    if st.button('Haal verwachte beschikbare fietsen op'):
        input_json = {"locatie":station,
                      "datum":datum,
                      "tijd":tijd}

        response = requests.request("POST", url, json=input_json)
        st.write(response.text)

    else:
        return



