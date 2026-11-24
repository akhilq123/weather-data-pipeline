import requests
import json


locations = {
    "Toronto": {
        "latitude": 43.6532,
        "longitude": -79.3832,
        "timezone": "America/Toronto"
    },
    "Mississauga": {
        "latitude": 43.5890,
        "longitude": -79.6441,
        "timezone": "America/Toronto"
    },
    "Kochi": {
        "latitude": 9.9312,
        "longitude": 76.2673,
        "timezone": "Asia/Kolkata"
    },
    "Neriamangalam": {
        "latitude": 10.056,
        "longitude": 76.737,
        "timezone": "Asia/Kolkata"
    }
}

def api_call(latitude, longitude, timezone):
    try:
        url=f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max&timezone={timezone}&forecast_days=1"
        r=requests.get(url, timeout=30)
        r.raise_for_status()
        print("success")
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"API request Failed : {e}")
        return None

record1 = {
    "location": "Toronto",
    "date": "2026-11-24"
}

record2 = {
    "location": None,
    "date": "2026-11-24"
}

def validate_weather(record):
    if record["location"] is not None and record["date"] is not None and \
        record["temperature_max"]>=record["temperature_min"] \
        and record["precipitation"]>=0 and record["wind_speed_max"]>=0:
        return True
    else:
         return False

if __name__=="__main__":
    print(validate_weather(record2))
    weather_records=[]
    raw_weather_records=[]
    for location in locations:
        latitude=locations[location]["latitude"]
        longitude=locations[location]["longitude"]
        timezone=locations[location]["timezone"]
        data=api_call(latitude,longitude,timezone)
        if data is not None:
            weather_record={}
            raw_weather_records.append(data)

            weather_record["location"]=location
            weather_record["date"] = data['daily']['time'][0]
            weather_record["temperature_max"] = data['daily']['temperature_2m_max'][0]
            weather_record["temperature_min"] = data['daily']['temperature_2m_min'][0]
            weather_record["precipitation"] = data['daily']['precipitation_sum'][0]
            weather_record["wind_speed_max"] = data['daily']['wind_speed_10m_max'][0]
            weather_records.append(weather_record)

    
    # with open("data/raw/weather.json","w") as file:
    #     json.dump(data,file,indent= 4)
    with open("data/processed/weather.json","w") as file:
        json.dump(weather_records,file,indent=4)
    with open("data/raw/weather.json","w") as file:
                json.dump(raw_weather_records,file,indent=4)
    # {'latitude': 43.646603, 'longitude': -79.38272, 'generationtime_ms': 0.09882450103759766, 'utc_offset_seconds': -18000, 'timezone': 'America/Toronto', 'timezone_abbreviation': 'GMT-5', 'elevation': 99.0,
    #   'daily_units': {'time': 'iso8601', 'temperature_2m_max': '°C', 'temperature_2m_min': '°C', 'precipitation_sum': 'mm', 'wind_speed_10m_max': 'km/h'}, 
    #   'daily': {'time': ['2026-11-24'], 'temperature_2m_max': [2.7], 'temperature_2m_min': [-3.8], 'precipitation_sum': [0.0], 'wind_speed_10m_max': [14.5]}}