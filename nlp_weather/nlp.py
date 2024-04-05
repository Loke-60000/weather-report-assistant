import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from gtts import gTTS
import base64
from fastapi import Body


from hidden import DATABASE, USER, PASSWORD, HOST, PORT, api_key, provider, model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


def fetch_weather_data(session, city):
    weather_data = session.query(MeteoFrance).filter_by(
        city=city).order_by(MeteoFrance.date.desc()).limit(1).first()
    if weather_data:
        print(f"Last weather data found for {city}:")
        print(f"Date: {weather_data.date}")
        print(f"Temperature: {weather_data.temperature}")
    else:
        print(f"No weather data found for {city}.")
    return weather_data


connection_string = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
session = Session()


city = "Paris"
weather_data = fetch_weather_data(session, city)


@app.post("/chat")
def chat(message: Optional[str] = None, city: str = Body(..., embed=True)):
    user_message = message if message else ''
    global weather_data
    weather_data = fetch_weather_data(session, city)

    ai_context = "You are a weather reporter. You are assisting a user with weather information."
    if weather_data:
        weather_info = f" Last weather data found for {weather_data.city}:"
        weather_info += f" Date: {weather_data.date.strftime('%Y-%m-%d %H:%M:%S')}"
        weather_info += f" Temperature: {weather_data.temperature}°C"
        weather_info += f" Humidity: {weather_data.humidity}%"
        weather_info += f" Rain: {weather_data.rain}"
        weather_info += f" Snow: {weather_data.snow}"
        weather_info += f" Clouds: {weather_data.clouds}%"
        weather_info += f" Wind: {weather_data.wind}"
        weather_info += f" Weather description: {weather_data.weather_desc}"
        weather_info += f" Weather icon: {weather_data.weather_icon}"
        weather_info += f" Readable warnings: {weather_data.readable_warnings}"

    else:
        weather_info = f" No weather data found for {city}."

    ai_context += weather_info

    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api.edenai.run/v2/text/chat"

    payload = {
        "providers": provider,
        "model": model,
        "text": ai_context + user_message,
        "chatbot_global_action": ai_context,
        "temperature": 0.8,
        "max_tokens": 150,
        "fallback_providers": ""
    }

    def get_audio(text):
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        with open("response.mp3", "rb") as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')
        return encoded_audio

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()
        generated_text = result['openai']['generated_text']
        response_text = generated_text

        audio = get_audio(response_text)

        return JSONResponse(content={"response": response_text, "weather_info": weather_info, "audio": audio})
    else:
        return JSONResponse(content={"error": "Failed to get response from the API"}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
