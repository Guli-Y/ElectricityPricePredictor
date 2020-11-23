# -*- coding: UTF-8 -*-

# Import from standard library
import os
import electricity_price_predictor
import pandas as pd
# Import from our lib
from electricity_price_predictor.lib import clean_data
import pytest


def test_clean_data():
    datapath = os.path.dirname(os.path.abspath(electricity_price_predictor.__file__)) + '/data'
    df = pd.read_csv('{}/data.csv.gz'.format(datapath))
    first_cols = ['id', 'civility', 'birthdate', 'city', 'postal_code', 'vote_1']
    assert list(df.columns)[:6] == first_cols
    assert df.shape == (999, 142)
    out = clean_data(df)
    assert out.shape == (985, 119)
