from meteofrance_api import MeteoFranceClient
from cities import cities
from functions.db_and_table_init import connect_to_database, create_table
from functions.insert_data import insert_weather_data
from functions.delete_data import delete_former_data


def run_daily_batch():
    client = MeteoFranceClient()
    conn = connect_to_database()
    create_table(conn)
    for c in cities:
        list_places = client.search_places(c)
        if list_places:
            my_place = list_places[0]

            my_place_weather_forecast = client.get_forecast_for_place(my_place)
            if my_place_weather_forecast and hasattr(my_place_weather_forecast, 'forecast'):
                my_place_hourly_forecast = my_place_weather_forecast.forecast

                for hour in my_place_hourly_forecast:
                    insert_weather_data(
                        conn, client, my_place, my_place_weather_forecast, hour)

    delete_former_data(conn)
    conn.commit()
    conn.close()


run_daily_batch()
