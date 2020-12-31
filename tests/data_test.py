# -*- coding: UTF-8 -*-

import os
import pandas as pd
from electricity_price_predictor.data import get_updated_price, get_shifted_price
from datetime import date


def test_get_shifted_price():
    location = f'gs://electricity_price_predictor/data/updated_price.csv'
    df = pd.read_csv(location, parse_dates=True, index_col='time')
    today = date.today()
    assert df.index[-1] >= today
    assert df.price.isnull().sum() == 6
    df_shifted = get_shifted_price(df=df)
    assert df_shifted.price.isnull().sum() == 0
