import requests
from datetime import datetime
from os import getenv
import json


async def get(city: str, date: datetime) -> str:
    """
    Request data from weather API and return forecast string
    """

    API_KEY = getenv("WEATHER_API_KEY")
    url = "https://api.openweathermap.org/data/2.5/forecast?lang=eng&units=metric" \
         "&q=%s" \
         "&appid=%s" \
         % (city, API_KEY)
    r = requests.get(url)

    if not r.status_code == requests.codes.ok:
        return False

    json_data = json.loads(r.text)
    fcast_str = fcast_format(json_data, date)
    return fcast_str


def fcast_format(data: json, date: datetime) -> str:
    """
    Format forecast data piece from json to string
    """
    fcast_data = []
    date_str = date.strftime('%Y-%m-%d')
    for item in data["list"]:
        if "12:00:00" in item["dt_txt"] and date_str in item["dt_txt"]:
            fcast_data.append(item)
            break
    temp = fcast_data[0]["main"]["temp_max"]
    descr = fcast_data[0]["weather"][0]["main"]
    wind_speed = fcast_data[0]["wind"]["speed"]
    s = "Temperature: %s°C\n" \
        "%s\n" \
        "Wind speed: %s m/s" % (temp, descr, wind_speed)
    return s
    # Data example
        # "cod":"200","message":0,"cnt":40,"list":[
        #                                         {"dt":1701885600,
        #                                               "main":
        #                                                                 {"temp":-9.52,
        #                                                                  "feels_like":-9.52,
        #                                                                  "temp_min":-21.97,
        #                                                                  "temp_max":-9.52,
        #                                                                  "pressure":1036,
        #                                                                  "sea_level":1036,
        #                                                                  "grnd_level":1016,
        #                                                                  "humidity":100,
        #                                                                  "temp_kf":12.45
        #                                                                  },
        #                                          "weather":[
        #                                              {"id":803,
        #                                               "main":"Clouds",
        #                                               "description":"broken clouds",
        #                                               "icon":"04n"}
        #                                          ],
        #                                          "clouds":{
        #                                               "all":80
        #                                          },
        #                                          "wind":{
        #                                               "speed":0.7,
        #                                               "deg":93,
        #                                               "gust":0.71
        #                                          },
        #                                          "visibility":3534,
        #                                          "pop":0,
        #                                          "sys":{"pod":"n"},
        #                                          "dt_txt":"2023-12-06 21:00:00"
        #                                          }