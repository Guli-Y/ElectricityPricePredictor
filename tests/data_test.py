# -*- coding: UTF-8 -*-

import os
import electricity_price_predictor
import pandas as pd
from electricity_price_predictor.data import get_shifted_price
from datetime import date
import pytest


def test_get_shifted_price():
    path = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(path, '..', 'data','updated_price.csv')
    df = pd.read_csv(file, parse_dates=True, index_col='time')
    today = date.today()
    assert df.index.date()[-1] >= today
    assert df.price.isnull().sum()[0] == 6
    df_shifted = get_shifted_price(df)
    assert df_shifted.price.isnull().sum()[0] == 0
