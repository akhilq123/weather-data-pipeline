def validate_weather(record):
    if record["location"] is not None and record["date"] is not None and \
        record["temperature_max"]>=record["temperature_min"] \
        and record["precipitation"]>=0 and record["wind_speed_max"]>=0:
        return True
    else:
         return False