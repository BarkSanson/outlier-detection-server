from dataclasses import dataclass

@dataclass
class DetectionRequest:
    station_id: str
    n_samples: int
    samples: list[dict]

    @staticmethod
    def from_json(data: dict):
        return DetectionRequest(
            station_id=data["id_estacio"],
            n_samples=data["numero_mostres"],
            samples=data["mostres"]
        )
