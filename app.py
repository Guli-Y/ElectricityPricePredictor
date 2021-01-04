import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from datetime import date, timedelta
import base64

st.set_page_config(page_title="electricity-price-predictor",
                    page_icon=":zap:",
                    layout="centered", # wide
                    initial_sidebar_state="expanded") # collapsed


### sidebar
st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#2e7bcf,#2e7bcf);
    color: blue;
}
</style>
""", unsafe_allow_html=True)
st.sidebar.markdown("""
    <style>
        #title {color: red;
        font-size: 36px;
        text-align: right;}
    </style>
<b id="title"> Wagon Energy <br>
:zap::zap::zap::zap::zap: </b>
    """, unsafe_allow_html=True)
st.sidebar.markdown("""
     <style>
        #subtitle {color: red;
        font-size: 24px}
    </style>
     <b id="subtitle"> Powering up your life </b>
    """, unsafe_allow_html=True)

image = Image.open('grid.jpg')
st.sidebar.image(image, use_column_width=True)


# title
st.title("Electricity Price Predictor")
st.markdown("Bidding zone: DK1")
st.markdown('<style>h1{color: black}</style>', unsafe_allow_html=True)
st.markdown("Map of Denmark showing bidding zones of the energy market")
image = Image.open("DK1.png")
st.image(image, caption='map', use_column_width=True)

# loading forecast data
today = date.today()
forecast_data = f'https://storage.googleapis.com/electricity_price_predictor/forecast/forecast_{today}.csv'
df = pd.read_csv(forecast_data)

# showing forecast figure and data side by side
st.markdown("Table 1 - DK1 " + str(df.date_time[0][:10]) + " - Hourly Electricity Price")
col1, col2 = st.beta_columns([6,2])

with col1:
    st.line_chart(df['price'])

with col2:
    st.write(df['price'])

# forecast figure including day ahead price and twoday_ahead price
forecast_fig = f'https://storage.googleapis.com/electricity_price_predictor/forecast/forecast_{today}.png'
st.image(forecast_fig, aption= 'Inventory Planner', width=1000)

### Creating a link to download the data or plot
st.markdown("""Click the link below to download the data in csv format""")
def get_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="{today}.csv">Download csv file</a>'

st.markdown(get_download_link(df), unsafe_allow_html=True)
