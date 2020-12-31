import numpy as np

def get_mape(y_true, y_pred):
    '''it takes two lists or pd.series (y_true, y_pred) and returns
    mean absolute percentage error'''
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    mape = np.round(mape,2)
    return f'{mape}%'

def get_mase(y_true, y_pred, train_y):
    '''it takes two lists or pd.series (y_true, y_pred) and returns
    mean absolute scaled error'''
    y_true, y_pred, train_y = np.array(y_true), np.array(y_pred), np.array(train_y)
    upper = np.mean(np.abs(y_pred-y_true))
    train_t = train_y[:-1]
    train_t_1 = train_y[1:]
    lower = np.mean(np.abs(train_t-train_t_1))
    mase = np.round(upper/lower, 2)
    return str(mase)
