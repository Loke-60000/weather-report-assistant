import json
from datetime import datetime
from meteofrance_api.helpers import readeable_phenomenoms_dict
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MeteoFrance(Base):
    __tablename__ = 'french_cities_weather'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    date = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)
    rain = Column(String)
    snow = Column(String)
    clouds = Column(Integer)
    wind = Column(String)
    weather_desc = Column(String)
    weather_icon = Column(String)
    readable_warnings = Column(String)

def insert_weather_data(session, client, my_place, my_place_weather_forecast, hour):
    date = datetime.fromtimestamp(hour['dt'])

    readable_warnings = "No weather alerts available."
    weather_desc = "No weather description available."
    weather_icon = "No weather icon available."
    snow = "No snow forecast available."
    rain = "No rain forecast available."
    wind = "No wind forecast available."
    clouds = "No cloud forecast available."

    if my_place_weather_forecast.position.get('rain_product_available'):
        if my_place.admin2 and len(my_place.admin2) < 3:
            my_place_weather_alerts = client.get_warning_current_phenomenoms(
                my_place.admin2
            )
            readable_warnings = readeable_phenomenoms_dict(
                my_place_weather_alerts.phenomenons_max_colors
            )

    weather_data = MeteoFrance(
        city=my_place.name,
        latitude=my_place_weather_forecast.position['lat'],
        longitude=my_place_weather_forecast.position['lon'],
        date=date,
        temperature=hour['T']['value'],
        humidity=hour['humidity'],
        rain=json.dumps(hour['rain']) if isinstance(hour['rain'], dict) else rain,
        snow=json.dumps(hour['snow']) if isinstance(hour.get('snow'), dict) else snow,
        clouds=hour['clouds'] if isinstance(hour['clouds'], int) else clouds,
        wind=json.dumps(hour['wind']) if isinstance(hour['wind'], dict) else wind,
        weather_desc= hour['weather']['desc'] if isinstance(hour['weather'], dict) else weather_desc,
        weather_icon= hour['weather']['icon'] if isinstance(hour['weather'], dict) else weather_icon,
        readable_warnings=json.dumps(readable_warnings)
    )

    if (weather_data.date.date() - datetime.now().date()).days < 4:
        print(f"Inserting data for {weather_data.city} on {weather_data.date.date()} at {weather_data.date.time()}.")
        session.add(weather_data)
        session.commit()
    else:
        print(f"Skipping data for {weather_data.city} on {weather_data.date.date()} at {weather_data.date.time()} as it is already in the table.")
