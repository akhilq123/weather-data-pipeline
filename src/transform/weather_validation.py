from datetime import datetime

def validate_date(date):
    try: 
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False

def validate_weather(record):
    if "location" in record and "date" in record and "temperature_max" in record and "temperature_min" in record and "precipitation" in record and "wind_speed_max" in record \
        and isinstance(record["temperature_max"], (int, float)) and isinstance(record["temperature_min"], (int, float)) \
            and isinstance(record["precipitation"], (int, float)) and isinstance(record["wind_speed_max"], (int, float)) \
                and isinstance(record["location"], str) and record.get("location").strip() !=""  \
             and record["temperature_max"]>=record["temperature_min"] \
            and record["precipitation"]>=0 and record["wind_speed_max"]>=0 and validate_date(record["date"]):
        return True
    return False

