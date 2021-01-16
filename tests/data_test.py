# -*- coding: UTF-8 -*-
import pandas as pd
from electricity_price_predictor.data import get_shifted_price
from datetime import date


def test_get_shifted_price():
    location = 'https://storage.googleapis.com/electricity_price_predictor/data/updated_price.csv'
    df = pd.read_csv(location, parse_dates=True, index_col='time')
    assert df.price.isnull().sum() == 6
    df_shifted = get_shifted_price(df=df)
    assert df_shifted.price.isnull().sum() == 0
