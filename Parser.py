import requests
import time
import datetime
from typing import List, Dict, Tuple


LATITUDE = 59.894
LONGITUDE = 30.264
API_KEY = 'b3db395bfcab2330526d3c26266ec1d8'


def date() -> List[int]:
    date_list = []
    current_midnight = datetime.date.today()
    unixtime = time.mktime(current_midnight.timetuple())
    for _ in range(5):
        date_list.append(int(unixtime))
        unixtime -= 86400
    return date_list


def converted_time(sunrise: int, sunset: int) -> datetime.timedelta:
    sunrise = datetime.datetime.fromtimestamp(sunrise)
    sunset = datetime.datetime.fromtimestamp(sunset)
    return sunset - sunrise


def get_weather(api_key: str, lat: float, lon: float, dates: List[int]) -> Tuple:
    temp_difference = dict()
    day_hours = dict()
    for day in dates:
        url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={time}&' \
              'appid={API_key}&units=metric'.format(lat=lat, lon=lon, time=day, API_key=api_key)
        response = requests.get(url).json()
        temp_difference[day] = round((response['current']['temp'] - response['current']['feels_like']), 3)
        day_hours[day] = converted_time(response['current']['sunrise'], response['current']['sunset'])
    return temp_difference, day_hours


def temperature_difference(temp: Dict) -> None:
    sorted_temp = dict(sorted(temp.items(), key=lambda item: item[1]))
    day = list(sorted_temp.keys())[0]
    date = datetime.datetime.fromtimestamp(day)
    print('За последние 5 дней минимальная разница между ощущаемой и фактической '
          'температурой была {date}, и составила {temp} градусов '
          'Цельсия'.format(date=date.date(), temp=sorted_temp[day]))


def daylight_hours(day_light: Dict) -> None:
    sorted_day = dict(sorted(day_light.items(), key=lambda item: item[1], reverse=True))
    day = list(sorted_day.keys())[0]
    date = datetime.datetime.fromtimestamp(day)
    print('За последние 5 дней максимальная продолжительность светового дня '
          'была {date}, и составила {time}'.format(date=date.date(), time=sorted_day[day]))


dates = date()
temp_diff, dayli_hours = get_weather(API_KEY, LATITUDE, LONGITUDE, dates)
temperature_difference(temp_diff)
daylight_hours(dayli_hours)
