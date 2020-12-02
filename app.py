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
    initial_sidebar_state="auto") # collapsed


raiden = Image.open('raiden.jpg')
st.sidebar.markdown(f"""
    # RAIDEN ENERGY
    """)

# font_size = st.sidebar.slider('Changer header size', 16, 72, 36)

SIDEBAR_CSS = f"""
<h1 style=“font-size:44px;
color:blue>
"""

### Creating the sidebar
st.sidebar.image(raiden, use_column_width=True)
st.write(SIDEBAR_CSS, unsafe_allow_html=True)


TITLE_CSS = f"""
<h1 style=“font-size:44px;
color:rgb(0,0,152)“>
"""


st.title("ELECTRA PROJECT")
st.write(TITLE_CSS, unsafe_allow_html=True)
st.markdown("## Day Ahead Electricity Price Predictor ")
st.markdown('<style>h1{color: blue;}</style>', unsafe_allow_html=True)
###




### Table 1, price prediction
st.markdown("Table 1 - DK1 4th of December - Electricity Prices")
@st.cache
def get_dataframe_data():
    print('get_dataframe_data called')
    return pd.DataFrame(
            np.random.randn(24, 1),
            columns=('col %d' % i for i in range(1))

        )

df = get_dataframe_data()

### Line chart function
@st.cache
def get_line_chart_data():
    print('get_line_chart_data called')
    return pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c']
        )
###


#### Ploting the table and chart side by side
col1, col2 = st.beta_columns([1,4])

with col1:
    st.write(df, use_column_width=True)
with col2:
    st.line_chart(df)

###



### Table 2, price prediction
st.markdown("Table 2 - 5th of December, Electricity Prices")
@st.cache
def get_dataframe_data():
    print('get_dataframe_data called')
    return pd.DataFrame(
            np.random.randn(24, 1),
            columns=('col %d' % i for i in range(1))
        )

df1 = get_dataframe_data()

# st.dataframe(df1.head().style.highlight_max(axis=0))
###


#### Ploting the table and chart side by side
col1, col2 = st.beta_columns([1,4])

with col1:
    st.write(df1, use_column_width=True)
with col2:
    st.line_chart(df)

###



### Creating a link to download the data or plot

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
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


st.markdown("""
    Click the [link](https://pricepred-g.herokuapp.com/) to check the price prediction on the web app
    """)
###



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


image = Image.open('test.png')

st.image(image, use_column_width=True)

# def get_map_data():
#     print('get_map_data called')
#     return pd.DataFrame(
#             np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#             columns=['lat', 'lon']
#         )

# if st.checkbox('Show map', False):
#     df = get_map_data()

#     st.map(df)
# else:
#     from PIL import Image
#     image = Image.open("DK1.png")
#     st.image(image, caption='map', use_column_width=False)









