import pytest
from functions.db_and_table_init import connect_to_database
from meteofrance_api.helpers import readeable_phenomenoms_dict
from meteofrance_api import MeteoFranceClient
from meteofrance_api import MeteoFranceClient

city_list = ["Paris", "Montpellier", "Lyon", "Marseille", "Toulouse",]

@pytest.fixture
def test_connect_to_database():
    conn = connect_to_database()
    assert conn is not None, "Connection to the database failed."


@pytest.mark.parametrize("city", city_list)
def test_search_places(city: str) -> None:
    client = MeteoFranceClient()
    list_places = client.search_places(city)
    assert list_places


@pytest.mark.parametrize("city", city_list)
def test_get_forecast_for_place(city: str) -> None:
    client = MeteoFranceClient()
    list_places = client.search_places(city)
    my_place = list_places[0]
    my_place_weather_forecast = client.get_forecast_for_place(my_place)
    assert my_place_weather_forecast


@pytest.mark.parametrize("city", city_list)
def test_get_daily_forecast_for_place(city: str) -> None:
    client = MeteoFranceClient()
    list_places = client.search_places(city)
    my_place = list_places[0]
    my_place_weather_forecast = client.get_forecast_for_place(my_place)
    my_place_daily_forecast = my_place_weather_forecast.daily_forecast
    assert isinstance(my_place_daily_forecast, list)


@pytest.mark.parametrize("city", city_list)
def test_get_rain_forecast(city: str) -> None:
    """
    Test if the rain forecast is available for the given city.
    """
    client = MeteoFranceClient()
    list_places = client.search_places(city)
    my_place = list_places[0]
    my_place_weather_forecast = client.get_forecast_for_place(my_place)
    if my_place_weather_forecast.position["rain_product_available"] == 1:
        my_place_rain_forecast = client.get_rain(
            my_place.latitude, my_place.longitude)
        next_rain_dt = my_place_rain_forecast.next_rain_date_locale()
        rain_status = next_rain_dt.strftime(
            "%H:%M") if next_rain_dt else "No rain expected in the following hour."
    else:
        rain_status = "No rain forecast available."
    assert rain_status


@pytest.mark.parametrize("city", city_list)
def test_get_weather_warnings(city: str) -> None:
    """
    Test if the weather warnings are available for the given city.
    """
    client = MeteoFranceClient()
    list_places = client.search_places(city)
    my_place = list_places[0]
    readable_warnings = {}
    if my_place.admin2:
        my_place_weather_alerts = client.get_warning_current_phenomenoms(
            my_place.admin2)
        readable_warnings = readeable_phenomenoms_dict(
            my_place_weather_alerts.phenomenons_max_colors)
    assert isinstance(readable_warnings, dict)


def test_connect_to_database():
    conn = connect_to_database()
    assert conn is not None, "Connection to the database failed."
