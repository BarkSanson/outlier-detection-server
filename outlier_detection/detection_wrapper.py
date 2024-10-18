import numpy as np

from online_outlier_detection.pipelines import MKWIForestBatchPipeline
from .outlier_response import VariableOutliers, OutlierResponse
from .station_data import StationData

SCORE_THRESHOLD = 0.8
ALPHA = 0.05
SLOPE_THRESHOLD = 0.1
WINDOW_SIZE = 128


class DetectionWrapper:
    def __init__(self):
        self.date_buffer = np.array([])
        self.pipelines = {field.name: MKWIForestBatchPipeline(
                score_threshold=SCORE_THRESHOLD,
                alpha=ALPHA,
                slope_threshold=SLOPE_THRESHOLD,
                window_size=WINDOW_SIZE) for field in StationData.get_fields() if field.name not in ["date"]}

    def update(self, data: StationData) -> OutlierResponse | None:
        self.date_buffer = np.append(self.date_buffer, data.date)

        results = {}

        for field in StationData.get_fields():
            if field.name == "date":
                continue

            results[field.name] = self.pipelines[field.name].update(getattr(data, field.name))

        if np.all([result is None for result in results.values()]):
            return None

        final_result = OutlierResponse()

        for variable, result in results.items():
            _, labels = result
            if not np.any(labels == 1):
                continue

            outlier_indices = np.where(labels == 1)[0]

            outliers = VariableOutliers(type=variable, dates=list(self.date_buffer[outlier_indices]))

            final_result.add_outlier(outliers)

        self.date_buffer = np.array([])

        if len(final_result) == 0:
            return None

        return final_result

