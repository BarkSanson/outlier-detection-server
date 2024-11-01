from dataclasses import dataclass

@dataclass
class StationOutlierRequest:
    id_station: str
    variables: dict[str, list]

    @staticmethod
    def from_json(data: dict):
        id_station = data["id_estacio"]
        variables = {
            variable: values
            for variable, values in data["variables"].items()
            if variable != "date" and variable != "id_estacio"
        }

        return StationOutlierRequest(
            id_station=id_station,
            variables=variables
        )


@dataclass
class DetectionRequest:
    requests: list[StationOutlierRequest]

    @staticmethod
    def from_json(data: list):
        return DetectionRequest(
            requests=[StationOutlierRequest.from_json(request) for request in data]
        )