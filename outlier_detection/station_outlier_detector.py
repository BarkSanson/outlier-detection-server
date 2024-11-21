from dataclasses import dataclass

from outlier_detection.variable_detector import VariableDetector


@dataclass
class VariableOutliers:
    station_id: str
    variable: str
    dates: list[str]

    def to_json(self):
        return {
            "station_id": self.station_id,
            "variable": self.variable,
            "dates": self.dates
        }


class OutliersDetected:
    def __init__(self):
        self.outliers: list[VariableOutliers] = []

    def add_outlier(self, outliers: VariableOutliers):
        self.outliers.append(outliers)

    def to_json(self):
        return [outlier.to_json() for outlier in self.outliers]

    def __len__(self):
        return len(self.outliers)

class StationOutlierDetector:
    def __init__(
            self,
            station_id: str,
            variables: dict):
        self.station_id = station_id
        self.timestamp_buffer = []

        self.detectors = {
            variable: VariableDetector(station_id=self.station_id, variable=variable, window_size=window_size)
            for variable, window_size in variables.items()
        }

    def update(self, data: dict) -> OutliersDetected | None:
        results = {}

        for variable, x in data.items():
            if variable not in self.detectors:
                continue

            results[variable] = self.detectors[variable].update(x)

        final_result = OutliersDetected()

        for variable, outliers in results.items():
            if outliers is None:
                continue

            final_result.add_outlier(VariableOutliers(
                station_id=self.station_id,
                variable=variable,
                dates=outliers
            ))

        return final_result if len(final_result) > 0 else None
