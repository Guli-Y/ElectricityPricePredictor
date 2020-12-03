# from flask import Flask, escape, request
# import joblib

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     # get param from http://127.0.0.1:5000/?name=value
#     name = request.args.get("name", "World")
#     return f'Hello, {escape(name)}!'

# @app.route('/predict_price')
# def day_head():
#     test = joblib.load('../test_testset.joblib')

#     model = joblib.load('../test_model.joblib')
#     pred = model.predict(test)[0]

#     return {'test_values': test, 'day-ahead prediction': pred}


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


### New changes from Ismael

st.markdown(
    """
<style>
.sidebar{
    background-color: rgb(0,0,255);
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


### New changes from Ismael

st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: rgb(0,0,255);
}
</style>
""",
    unsafe_allow_html=True,
)



st.title("ELECTRA PROJECT")
# st.write(TITLE_CSS, unsafe_allow_html=True)
st.markdown("## Electricity Price Predictor for Denmark ")
st.markdown('<style>h1{color: black}</style>', unsafe_allow_html=True)
###

st.markdown("Map of Denmark showing bidding zones of the energy market")

image = Image.open("DK1_edited.png")
st.image(image, caption='map', use_column_width=True)


df = pd.read_csv('forecast_data/forecast_data.csv')



today = date.today()
today = str(today)
tomorrow = date.today() + timedelta(days=1)
tomorrow = str(tomorrow)



#### Ploting the table and chart side by side
st.markdown("Table 1 - DK1 " + today + " - Hourly Electricity Prices")
col1, col2 = st.beta_columns([4,1])

with col1:
    st.area_chart(df.loc[:24, 'price'])

with col2:
    st.write(df.loc[:24, 'price'], use_column_width=True)

###


df_half = df.loc[24:, 'price']
df_half = df_half.reset_index(drop=True)

###
st.markdown("Table 2 - DK2 " + tomorrow + " - Hourly Electricity Prices")
col1, col2 = st.beta_columns([4,1])



with col1:
    # st.line_chart(df_half)

    st.area_chart(df_half, use_container_width=True)

with col2:
    st.write(df_half, use_column_width=True)


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


