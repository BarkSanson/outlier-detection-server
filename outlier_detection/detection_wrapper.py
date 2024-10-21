import os.path
import pickle

import numpy as np

from online_outlier_detection.pipelines import MKWIForestBatchPipeline
from .outlier_response import VariableOutliers, OutlierResponse
from .station_data import StationData

SCORE_THRESHOLD = 0.8
ALPHA = 0.05
SLOPE_THRESHOLD = 0.1
WINDOW_SIZE = 256


class DetectionWrapper:
    def __init__(self):
        self.date_buffer = np.array([])
        self.pipelines = {field.name: MKWIForestBatchPipeline(
                score_threshold=SCORE_THRESHOLD,
                alpha=ALPHA,
                slope_threshold=SLOPE_THRESHOLD,
                window_size=WINDOW_SIZE) for field in StationData.get_fields() if field.name not in ["date"]}

        self._load_state()

    def update(self, data: StationData) -> OutlierResponse | None:
        self.date_buffer = np.append(self.date_buffer, data.date)

        results = {}

        for field in StationData.get_fields():
            if field.name == "date":
                continue

            results[field.name] = self.pipelines[field.name].update(getattr(data, field.name))

        self._save_state()

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

    def _load_state(self):
        if os.path.exists('./data/pipelines.pkl'):
            with open('./data/pipelines.pkl', 'rb') as f:
                self.pipelines = pickle.load(f)

        if os.path.exists('./data/dates.pkl'):
            with open('./data/dates.pkl', 'rb') as f:
                self.date_buffer = pickle.load(f)

    def _save_state(self):
        with open('./data/pipelines.pkl', 'wb') as f:
            pickle.dump(self.pipelines, f)

        with open('./data/dates.pkl', 'wb') as f:
            pickle.dump(self.date_buffer, f)

