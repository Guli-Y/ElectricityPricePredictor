
import os
import pandas as pd

def file_names(path='../'):
    csv_files = []
    for root, direc, files in os.walk('../'):
        if 'raw_data\\' in root:
            csv_files.append(files)
    return csv_files

def get_price(path='../raw_data/price/'):
    price_files = file_names()[2]
    df = pd.read_csv(path+price_files[0])
    for file in price_files[1:]:
        df_2 = pd.read_csv(path+file)
        df = pd.concat([df, df_2])
    df = df.reset_index(drop=True)
    df.columns = ['time', 'price']
    df['time'] = df.time.str[:16]
    df = df[df.price!='-'] # filtering the timestamps till 24.11.2020
    df['time'] = df.time.astype('datetime64')
    df['price'] = df.price.astype('float')
    return df

def get_shifted_price():
    df = get_price()
    df_1 = df.iloc[:2090, :]
    df_2 = df.iloc[2090:7132, :]
    df_3 = df.iloc[7132:10827, :]
    df_4 = df.iloc[10827:16037, :]
    df_5 = df.iloc[16037:19564, :]
    df_6 = df.iloc[19564:24774, :]
    df_7 = df.iloc[24774:28301, :]
    df_8 = df.iloc[28301:33511, :]
    df_9 = df.iloc[33511:37206, :]
    df_10 = df.iloc[37206:42248, :]
    df_11 = df.iloc[42248:45943, :]
    df_12 = df.iloc[45943:,]
    no_shift = [df_1, df_3, df_5, df_7, df_9, df_11]
    shift_list = [df_2, df_4,df_6, df_8, df_10, df_12]
    price_df = df_1.set_index('time')
    for data in no_shift[1:]:
        data.set_index('time', inplace=True)
        price_df = pd.concat([price_df, data])
    for data in shift_list:
        data.set_index('time', inplace=True)
        data = data.shift(periods=-1).dropna()
        price_df = pd.concat([price_df, data])
    return price_df


def get_load(path='../raw_data/load/'):
    load_files = file_names()[1]
    df = pd.read_csv(path+load_files[0])
    for file in load_files[1:]:
        df_2 = pd.read_csv(path+file)
        df = pd.concat([df, df_2])
    return df
