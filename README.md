# Project aim:    **Forecast Electricity Price for DK1**

This project was the final project of my team at Le Wagon Data Science Bootcamp.
The team members are the contributers of this repository.

This project is about developing a model for forecasting day-ahead electricity prices of biding zone DK1 (Denmark)
using data from Entose Transparency Platform and OpenWeatherMap. It includes data sourcing and exploration,
feature engineering, training time series model, evaluating model performance using walk-forward validation,
and continuious deployment on Heroku.
[forecast_validation_figure](walk_forward_validation_6m.png)

web app :point_right: https://electricity-price-predictor.herokuapp.com/

presentation :point_right: https://docs.google.com/presentation/d/1LzwVxNeJ9FzhfXJTaiTVQ-xDzbNQjwrejzYSZsak8YQ/edit?usp=sharing

demo day video (40:00 - 51:00) :point_right: https://youtu.be/mP9EG9zj6mo

# Data sources

**Day-ahead electricity price**

downloaded and API requested from [ENTSOE](https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/show?name=&defaultValue=true&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime=06.11.2020+00:00|CET|DAY&biddingZone.values=CTY|10Y1001A1001A83F!BZN|10Y1001A1001A82H&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2))

The clean, hourly, up-to-date electricity price data can be obtained by calling get_shifted_price() function from electricity_price_predictor.data.

**Historical weather of Denmark**

purchased from [openweather](https://openweathermap.org/)

Because I only have the licence for usage but not the ownership, I am not putting the data here.

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


For details about data exploration and model evaluation, please go to the notebooks.
