from dataclasses import dataclass, fields


@dataclass
class StationData:
    date: str
    solar_radiation: int
    precipitation: int
    lightning_strike_count: int
    lightning_strike_distance: int
    wind_speed: int
    wind_direction: int
    wind_speed_max: int
    air_temperature: int
    relative_humidity: int
    vapor_pressure: int
    barometric_pressure: int
    humidity_sensor_temperature: int
    tilt_north_south: int
    tilt_west_east: int

    @staticmethod
    def from_json(data: dict):
        mostra = data["mostra"]

        return StationData(
            date=data["date"],
            solar_radiation=mostra["solar_radiation"],
            precipitation=mostra["precipitation"],
            lightning_strike_count=mostra["lightningStrikeCount"],
            lightning_strike_distance=mostra["lightningStrikeDistance"],
            wind_speed=mostra["windSpeed"],
            wind_direction=mostra["windDirection"],
            wind_speed_max=mostra["windSpeedMax"],
            air_temperature=mostra["airTemperature"],
            relative_humidity=mostra["relativeHumidity"],
            vapor_pressure=mostra["vaporPressure"],
            barometric_pressure=mostra["barometricPressure"],
            humidity_sensor_temperature=mostra["humiditySensorTemperature"],
            tilt_north_south=mostra["tiltNorthSouth"],
            tilt_west_east=mostra["tiltWestEast"]
        )

    @staticmethod
    def get_fields():
        return fields(StationData)
