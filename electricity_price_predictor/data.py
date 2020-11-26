import os
import numpy as np
import pandas as pd

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
    df['time'] = pd.to_datetime(df['time'] , format="%d-%m-%Y %H%M", errors='ignore')


    return df

# Bringing it all together
#_________________________________________

def fetch_data(path):

    files = get_file_names(path)
    df_dict = get_dataframes(files)

    df = concat_dataframes(df_dict)
    df = get_datetime(df)

    # date up until
    idx = (df[df['time'] == '23.11.2020 23:00'].index)[0] + 1 # valid time frame
    df = df.iloc[:idx]

    try:
        df.drop(columns=['MTU (CET)'], inplace=True)
        df = df.rename(columns={'Day-ahead Price [EUR/MWh]':'price'})
        df = df[['time','price']]
    except:
        df.drop(columns=['Time (CET)'], inplace=True)
        df = df.rename(columns={'Actual Total Load [MW] - BZN|DK1':'load'})
        df = df[['time','load']]

    return df


