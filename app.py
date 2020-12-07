

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from datetime import date, timedelta
import base64


st.set_page_config(
    page_title="electricity price prediction",
    page_icon=":zap:",
    layout="centered", # wide
    initial_sidebar_state="expanded") # collapsed


### sidebar

st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#2e7bcf,#2e7bcf);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

st.sidebar.markdown("""
    <style>
        #title {color: black;
        font-size: 55px;
        text-align: right;}
    </style>
<b id="title"> :zap::zap::zap::zap: <br>
RAIDEN ENERGY <br>
:zap::zap::zap::zap: </b>
    """
    , unsafe_allow_html=True)


st.sidebar.markdown("""
     <style>
        #subtitle {color: black;
        font-size: 24px}
    </style>
     <b id="subtitle"> Powering up your life </b>
    """
    , unsafe_allow_html=True)

raiden = Image.open('raiden.jpg')
st.sidebar.image(raiden, use_column_width=True)


### title

st.title("ELECTRA PROJECT")
st.markdown("## Electricity Price Predictor for Denmark ")
st.markdown('<style>h1{color: black}</style>', unsafe_allow_html=True)
st.markdown("Map of Denmark showing bidding zones of the energy market")
image = Image.open("DK1_edited.png")
st.image(image, caption='map', use_column_width=True)

df = pd.read_csv('forecast_data/forecast_data.csv')



twoday_ahead = date.today() + timedelta(days=2)
twoday_ahead = str(today_2)

#### Ploting the table and chart side by side
st.markdown("Table 1 - DK1 " + twoday_ahead + " - Hourly Electricity Prices")
col1, col2 = st.beta_columns([4,1])

with col1:
    st.area_chart(df.loc[:23, 'price'])

with col2:
    st.write(df.loc[:23, 'price'], use_column_width=True)


image = Image.open('forecast_data/forecast.png')

st.image(image, use_column_width=True)

### Creating a link to download the data or plot

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
#     out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'

st.markdown("""Click the link below to download the data in csv format""")

st.markdown(
    get_table_download_link(df), unsafe_allow_html=True
    )
