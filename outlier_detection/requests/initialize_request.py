from dataclasses import dataclass


@dataclass
class InitializeRequest:
    station_id: str
    variables: dict

    @staticmethod
    def from_json(data: dict):
        return InitializeRequest(
            station_id=data["id_estacio"],
            variables=data["variables"]
        )