
from datetime import date
import time
from google.cloud import storage
from termcolor import colored
import os

BUCKET_NAME = 'electricity_price_predictor'

if __name__=='__main__':
    time.sleep(60*35)
    today = date.today()
    data = f'forecast/forecast_{today}.csv'
    fig = f'forecast/forecast_{today}.png'
    # instansiate storage client
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob1 = bucket.blob(data)
    location1 = f'gs://{BUCKET_NAME}/{data}'
    blob2 = bucket.blob(fig)
    location2 = f'gs://{BUCKET_NAME}/{fig}'
    # make the forecast data public
    blob1.make_public()
    blob2.make_public()
    print(colored(f'''forecast data and figure made public\n
        => {location1} \n
        => {location2}''', 'blue'))
