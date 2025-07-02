from FlightRadar24 import FlightRadar24API
from geopy.distance import geodesic


def render(draw, fonts, config):
    try:
        fr_api = FlightRadar24API()

        lat = config.get("lat")
        lon = config.get("lon")
        radius = config.get("radius")
        pos = config.get("pos", (60, 25))

# Точка интереса
        center_point = (lat, lon)

# Границы области
        bounds = fr_api.get_bounds_by_point(center_point[0], center_point[1], radius)

# Получаем рейсы
        flights = fr_api.get_flights(bounds=bounds)

# Фильтрация только тех, кто в воздухе
        flights_on_air = [f for f in flights if not f.on_ground]

# Функция для расчёта расстояния
        def get_distance(flight):
            return geodesic(center_point, (flight.latitude, flight.longitude)).meters

        if flights_on_air:
    # Поиск ближайшего
            nearest_flight = min(flights_on_air, key=get_distance)

            data = f"{nearest_flight.aircraft_code}: {nearest_flight.origin_airport_iata} -> {nearest_flight.destination_airport_iata}"
        else:
            data = "No flights in area"

        print(data)
        draw.text(pos, data, font=fonts["res"], fill=0)

    except Exception as e:
        draw.text(pos, "FR24 Err", font=fonts["res"], fill=0)
        print("[FlightRadar24] Error:", e)

