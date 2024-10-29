from dataclasses import dataclass, fields, asdict


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
        sample = data["mostra"]

        return StationData(
            date=data["date"],
            solar_radiation=sample["solar_radiation"],
            precipitation=sample["precipitation"],
            lightning_strike_count=sample["lightningStrikeCount"],
            lightning_strike_distance=sample["lightningStrikeDistance"],
            wind_speed=sample["windSpeed"],
            wind_direction=sample["windDirection"],
            wind_speed_max=sample["windSpeedMax"],
            air_temperature=sample["airTemperature"],
            relative_humidity=sample["relativeHumidity"],
            vapor_pressure=sample["vaporPressure"],
            barometric_pressure=sample["barometricPressure"],
            humidity_sensor_temperature=sample["humiditySensorTemperature"],
            tilt_north_south=sample["tiltNorthSouth"],
            tilt_west_east=sample["tiltWestEast"]
        )

    @staticmethod
    def get_fields():
        return fields(StationData)

    def __str__(self):
        return str(asdict(self))
