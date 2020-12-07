# -*- coding: UTF-8 -*-

# Import from standard library
from datetime import timedelta, date
from electricity_price_predictor.data import get_updated_price
import pytest


def test_get_updated_price():
    assert get_updated_price().index[-1].date() == date.today()+timedelta(days=1)
