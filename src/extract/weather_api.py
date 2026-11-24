import requests
import json

import logging
logging.basicConfig(
     filename="logs/weather-pipeline.log",
     level=logging.INFO,
     format="%(asctime)s - %(levelname)s - %(message)s"
)


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
        logging.error("API request failed: %s", e)
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
    weather_records=[]
    raw_weather_records=[]
    valid_records=[]
    invalid_records=[]
    logging.info("Weather extraction starting")
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

    logging.info("Weather extraction completed")
    with open("data/processed/weather.json","w") as file:
        json.dump(weather_records,file,indent=4)
    with open("data/raw/weather.json","w") as file:
                json.dump(raw_weather_records,file,indent=4)
    for weather_record in weather_records:
        if validate_weather(weather_record):
            valid_records.append(weather_record)
        else:
            invalid_records.append(weather_record)

    with open("data/processed/invalid_weather.json","w") as file:
          json.dump(invalid_records,file, indent=4)

    logging.info("Valid records = %s",len(valid_records))
    logging.info("Invalid records = %s",len(invalid_records))
    