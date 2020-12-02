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
import base64
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# from electricity_price_predictor.data import get_all, get_price
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.linear_model import LinearRegression
# import statsmodels.formula.api as sm




st.set_page_config(
    page_title="electricity price prediction",
    page_icon=":zap:",
    layout="centered", # wide
    initial_sidebar_state="collapsed") # collapsed


st.sidebar.markdown("""
    <font size="96">
        <span style=“color:white>
          <b>RAIDEN ENERGY</b>
        </span>
    </font>
    """
    , unsafe_allow_html=True)


raiden = Image.open('raiden.jpg')
st.sidebar.image(raiden, use_column_width=True)
# st.sidebar.markdown(f"""
#     # RAIDEN ENERGY
#     """)

# font_size = st.sidebar.slider('Changer header size', 16, 72, 36)

# SIDEBAR_CSS = f"""
# <h1 style=“font-size:44px;
# color:red>
# """

# ### Creating the sidebar

# st.write(SIDEBAR_CSS, unsafe_allow_html=True)


st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#2e7bcf,#2e7bcf);
    color: rgb(0,30,106);
}
</style>
""",
    unsafe_allow_html=True,
)



st.title("ELECTRA PROJECT")
# st.write(TITLE_CSS, unsafe_allow_html=True)
st.markdown("## Day Ahead Electricity Price Predictor ")
st.markdown('<style>h1{color: black}</style>', unsafe_allow_html=True)
###




### Table 1, price prediction
# st.markdown("Table 1 - DK1 4th of December - Electricity Prices")
# @st.cache
# def get_dataframe_data():
#     print('get_dataframe_data called')
#     return pd.DataFrame(
#             np.random.randn(24, 1),
#             columns=('col %d' % i for i in range(1))

#         )

df = pd.read_csv('forecast_data/forecast_data.csv')


# ### Line chart function
# @st.cache
# def get_line_chart_data():
#     print('get_line_chart_data called')
#     return pd.DataFrame(
#             np.random.randn(20, 3),
#             columns=['a', 'b', 'c']
#         )
# ###


#### Ploting the table and chart side by side
st.markdown("Table 1 - DK1 25th of November - Hourly Electricity Prices")
col1, col2 = st.beta_columns([1,3])

with col1:
    st.write(df.loc[:23, 'price'], use_column_width=True)
with col2:
    st.line_chart(df.loc[:23,'price'])

###


###
st.markdown("Table 2 - DK1 26th of November - Hourly Electricity Prices")
col1, col2 = st.beta_columns([1,3])

with col1:
    st.write(df.loc[23:, 'price'], use_column_width=True)
with col2:
    st.line_chart(df.loc[23:, 'price'])



image = Image.open('forecast_data/forecast.png')

st.image(image, use_column_width=True)

### Table 2, price prediction
# st.markdown("Table 2 - 5th of December, Electricity Prices")
# @st.cache
# def get_dataframe_data():
#     print('get_dataframe_data called')
#     return pd.DataFrame(
#             np.random.randn(24, 1),
#             columns=('col %d' % i for i in range(1))
#         )

# df1 = get_dataframe_data()

# st.dataframe(df1.head().style.highlight_max(axis=0))
###





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


# st.markdown("""
#     Click the [link](https://pricepred-g.herokuapp.com/) to check the price prediction on the web app
#     """)
# ###



# st.markdown("Progress bar")

# if st.checkbox('Show progress bar'):
#     import time

#     'Starting a long computation...'

#     # Add a placeholder
#     latest_iteration = st.empty()
#     bar = st.progress(0)

#     for i in range(100):
#         # Update the progress bar with each iteration.
#         latest_iteration.text(f'Iteration {i+1}')
#         bar.progress(i + 1)
#         time.sleep(0.1)

#     '...and now we\'re done!'


# test = joblib.load('test_testset.joblib')
# model = joblib.load('test_model.joblib')
# prediction = model.predict(test)
# st.write(prediction)


# if __name__ == "__main__":
#     #df = read_data()
#     main()


image = Image.open("DK1.png")
st.image(image, caption='map', use_column_width=True)









