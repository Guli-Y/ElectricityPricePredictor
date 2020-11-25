import os
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

def get_file_names(directory):
    """returns the csv files in the given string directory path"""
    file_names = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_names.append(os.path.join(directory, filename))
    return file_names

def get_dataframes(file_names):
    """Takes in a list of csv file paths.
    Returns a dictionary whose keys are the years
    and values are the corresponding dataframes."""
    df_years = {}
    for file in file_names:
        df_years[file[-29:]] = pd.read_csv(file) # [-29:] Indexes the years.csv eg '201501010000-201601010000.csv'
    return df_years

def get_feature_path(feature_name, main_directory):
    """Retrieve actual paths from by feature"""
    for root, dirs_, files in os.walk(main_directory):
        if feature_name in (root):
            return root

def get_features_df(main_path):
    """return dictionary of features 'price' and 'load'"""
    feats = ['price', 'load']
    feat_dict = {}
    for feat in feats:
        path = get_feature_path(feat, main_path)
        names = get_file_names(path)
        feat_dict[feat] = get_dataframes(names)

    return feat_dict[feats[0]], feat_dict[feats[1]]

def concat_dataframes(feat):
    """concatenate the years per feature to one huge dataframe"""
    keys = list(feat.keys())
    df = pd.concat([
        feat[keys[0]],  # year 2015
        feat[keys[1]],  # year 2016
        feat[keys[2]],  # year 2017
        feat[keys[3]],  # year 2018
        feat[keys[4]],  # year 2019
        feat[keys[5]]   # year 2020
    ]).reset_index(drop=True)
    return df

def get_datetime(df):
    """A function is created to make a new column called
    time that will strip the string down to the initial
    timestamp e.g 31.12.2020 19:00 from the initial
    31.12.2020 19:00 - 31.12.2020 format and then convert
    the series to datetime objects"""
    try:
        column = df['MTU (CET)'] # column with time values in price df
    except:
        column = df['Time (CET)']  # load time

    # create new column 'time' by formatting the original time column to get single timepoint instead of a range
    df['time'] = column.apply(lambda _: _[:16])
    # convert new time column from str to timestamp
    df['time'] = pd.to_datetime(df['time'])

    return df

def merge_data(feat_1, feat_2):
    df = feat_1.merge(feat_2, on='time').reset_index(drop=True)
    return df
#_________________________________________
# Bringing it all together
#_________________________________________

def fetch_data(path = r'../raw_data/'):

    price, load = get_features_df(main_path=path) # unpack tuple

    prices_data = concat_dataframes(price)
    load_data = concat_dataframes(load)

    load_data = get_datetime(load_data)
    prices_data = get_datetime(prices_data)

    # date up until
    idx_p = prices_data[prices_data['time'] == '2020-11-23 23:00:00'].index
    idx_l = load_data[load_data['time'] == '2020-11-23 23:00:00'].index
    assert(idx_p == idx_l)
    idx = idx_l[0] + 1

    df = merge_data(prices_data, load_data)
    df = df.iloc[:idx]

    # drop unused columns
    to_drop = ['MTU (CET)', 'Time (CET)', 'Day-ahead Total Load Forecast [MW] - BZN|DK1']
    df.drop(columns=to_drop, inplace=True)

    df = df.rename(columns={'Day-ahead Price [EUR/MWh]':'price',
                   'Actual Total Load [MW] - BZN|DK1':'load'})

    df = df[['time','price','load']] # reorder columns

    return df


