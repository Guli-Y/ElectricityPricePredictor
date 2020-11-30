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
import datetime
import pandas as pd
import numpy as np


date= st.date_input(
    "days for prediction",
    datetime.date(2020, 11, 19))

# time = st.time_input(
#     datetime.time(5,12))


st.markdown("Progress bar")

if st.checkbox('Show progress bar'):
    import time

    'Starting a long computation...'

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    '...and now we\'re done!'


st.markdown("Dataframe")
@st.cache
def get_dataframe_data():
    print('get_dataframe_data called')
    return pd.DataFrame(
            np.random.randn(10, 5),
            columns=('col %d' % i for i in range(5))
        )

df = get_dataframe_data()

st.write(df.head())

st.dataframe(df.head().style.highlight_max(axis=0))


st.markdown("Line Chart")

@st.cache
def get_line_chart_data():
    print('get_line_chart_data called')
    return pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c']
        )

df = get_line_chart_data()

st.line_chart(df)


@st.cache
def get_map_data():
    print('get_map_data called')
    return pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            columns=['lat', 'lon']
        )

if st.checkbox('Show map', False):
    df = get_map_data()

    st.map(df)
else:
    from PIL import Image
    image = Image.open('/raw_data/DK1.png')
    st.image(image, caption='map', use_column_width=False)


st.markdown("# ML Project - Electricity price predictor")





def main():
    print("hello")

if __name__ == "__main__":
    main()
