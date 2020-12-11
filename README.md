# Project aim:    **Forecast Electricity Price for DK1**

**This project was the final project of my team at Le Wagon Data Science Bootcamp. The team members are the contributers of this repository.**

**For the detailed description and evaluation of each model, please refere to the notebook of corresponding model in notebooks directory**

**If you are interested in our final presentation, please checkout this [slide](https://docs.google.com/presentation/d/1LzwVxNeJ9FzhfXJTaiTVQ-xDzbNQjwrejzYSZsak8YQ/edit?usp=sharing) and this [video]()**

**If you are interested in our forecast results, checkout our heroku [webpage](https://pricepred-g.herokuapp.com/)


# Data source

**Day-ahead electricity price**

downloaded and API requested from [ENTSOE](https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/show?name=&defaultValue=true&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime=06.11.2020+00:00|CET|DAY&biddingZone.values=CTY|10Y1001A1001A83F!BZN|10Y1001A1001A82H&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2))

The clean, hourly, up-to-date electricity price data can be obtained by calling get_shifted_price() function in data.py in electricity_price_predictor folder.

**Historical weather of Denmark**

purchased from [openweather](https://openweathermap.org/)

I could not make this data public becasue I only have the licence for usage but not the ownership.

**Future weather of Denmark**

requested from [openweather API](https://openweathermap.org/api)

# Feature selection

Features integrated into the sarimax:
1. wind_speed
2. holidays and the holiday is weekend
3. temperature
4. humidity

Features explored but did't contribute to forecasting accuracy:
1. clouds
2. load
3. total production
4. production by wind
5. wind production / total production

# Content of Repository

**data**
updated_price.csv : the historical electricity prices

**electricity_price_predictor**
data.py : all the functions used for data collection and preprocessing
sarima.py : functions for feature explorations, walk forward validation, ploting
sarimax.py : functions for forecasting and ploting

**forecast_data**
forecast.png : the plot showing day-ahead hourly prices and the forecasted 2day-ahead hourly prices
forecast_data.csv : the forecasted 2day-ahead hourly prices stored in csv

**notebooks**

sarimax_guli.ipynb : creation of sarimax model with detailed explanations. It includes data exploration, feature selection, walk forward validation, and forecast.
....
....

**scripts**

**tests**
data_test.py :

**app.py**

..............working on it.....................

The initial setup.

Create virtualenv and install the project:
```bash
  $ sudo apt-get install virtualenv python-pip python-dev
  $ deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
  $ make clean install test
```

Check for electricity_price_predictor in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/electricity_price_predictor`
- Then populate it:

```bash
  $ ##   e.g. if group is "{group}" and project_name is "electricity_price_predictor"
  $ git remote add origin git@gitlab.com:{group}/electricity_price_predictor.git
  $ git push -u origin master
  $ git push -u origin --tags
```

Functionnal test with a script:
```bash
  $ cd /tmp
  $ electricity_price_predictor-run
```
# Install
Go to `gitlab.com/{group}/electricity_price_predictor` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:
```bash
  $ sudo apt-get install virtualenv python-pip python-dev
  $ deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:
```bash
  $ git clone gitlab.com/{group}/electricity_price_predictor
  $ cd electricity_price_predictor
  $ pip install -r requirements.txt
  $ make clean install test                # install and test
```
Functionnal test with a script:
```bash
  $ cd /tmp
  $ electricity_price_predictor-run
```
