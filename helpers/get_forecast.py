import requests
from datetime import datetime
from os import getenv


def get(
        city: str,
        date: datetime,
) -> str:
    """
    Returns a formatted string with forecast
    """
    d = date.strftime('%d.%m.%Y')
    API_KEY = getenv("WEATHER_API_KEY")
    s = "https://api.openweathermap.org/data/2.5/weather?" \
        "name=%s" \
        "&appid=%s"\
        .format("moscow", API_KEY)
    r = requests.get(s)

    if not r.status_code == requests.codes.ok:
        return False

    return r.text[:50]