from dataclasses import dataclass

import numpy as np

from online_outlier_detection.pipelines import MKWIForestBatchPipeline

SCORE_THRESHOLD = 0.8
ALPHA = 0.05
SLOPE_THRESHOLD = 0.1

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

        self.pipelines = {variable: MKWIForestBatchPipeline(
            score_threshold=SCORE_THRESHOLD,
            alpha=ALPHA,
            slope_threshold=SLOPE_THRESHOLD,
            window_size=window_size) for variable, window_size in variables.items()}

    def update(self, data: dict[str, list]) -> OutliersDetected | None:
        results = {}

        for variable, data in data.items():
            if variable not in self.pipelines:
                continue

            # TODO: control cases where data is bigger than window size
            if len(data) > self.pipelines[variable].window_size:
                pass

            for x in data:
                result = self.pipelines[variable].update(x)

                if result is None:
                    continue

                _, labels, retrain = result

                # For research purposes, if there is a retrain, save the model. TODO
                if retrain:
                    self.pipelines[variable].save_state(f"data/{self.station_id}_{variable}_{data.date}.pkl")

                results[variable].extend(labels)

        final_result = OutliersDetected()

        for variable, labels in results.items():
            if labels is None:
                continue


            if not np.any(labels == 1):
                continue

            outlier_indices = np.where(labels == 1)[0]

            outliers = VariableOutliers(
                station_id=self.station_id,
                variable=variable,
                dates=list(data.date[outlier_indices]))

            final_result.add_outlier(outliers)

        return final_result

    def _load_state(self, path: str):
        # TODO
        pass
