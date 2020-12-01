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
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# from electricity_price_predictor.data import get_all, get_price
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.linear_model import LinearRegression
# import statsmodels.formula.api as sm

raiden = Image.open('raiden.jpg')
st.sidebar.markdown(f"""
    # RAIDEN ENERGY
    """)

# font_size = st.sidebar.slider('Changer header size', 16, 72, 36)

SIDEBAR_CSS = f"""
<h1 style=“font-size:44px;
color:red“>
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

st.write(df)

###

st.markdown("Line Chart")

@st.cache
def get_line_chart_data():
    print('get_line_chart_data called')
    return pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c']
        )

# df = get_line_chart_data()

st.line_chart(df)

### Table 2, price prediction
st.markdown("Table 2 - 5th of December, Electricity Prices")
@st.cache
def get_dataframe_data():
    print('get_dataframe_data called')
    return pd.DataFrame(
            np.random.randn(20, 2),
            columns=('col %d' % i for i in range(2))
        )

df1 = get_dataframe_data()

st.dataframe(df1.head().style.highlight_max(axis=0))
###

st.markdown("""[links](https://pricepred-g.herokuapp.com/)
    """)



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







# img = mpimg.imread('/notebooks/DK1.png')
# # plt.imshow(img)

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



col1, col2 = st.beta_columns([1,4])

with col1:
    st.write(df, use_column_width=True)
with col2:
    st.line_chart(df)





