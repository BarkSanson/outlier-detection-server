import os
import pickle
from datetime import datetime

import numpy as np

from online_outlier_detection.pipelines import MKWIForestBatchPipeline

SCORE_THRESHOLD = 0.8
ALPHA = 0.05
SLOPE_THRESHOLD = 0.1

class VariableDetector:
    def __init__(self, station_id, variable, window_size):
        self.station_id = station_id
        self.variable = variable
        self.window_size = window_size
        self.model = self._load_model()
        self.timestamp_buffer = []

    def update(self, data: dict) -> list | None:
        """
        Update the model with the new data.
        :param data: dictionary with the following structure:

        {
            "data": [0.1, 0.2],
            "dates": ["2021-09-01T00:00:00", "2021-09-01T00:00:01"]
        }

        :return: list of dates with detected outliers
        """
        results = []
        for x, timestamp in zip(data["data"], data["dates"]):
            self.timestamp_buffer.append(timestamp)
            result = self.model.update(x)

            if result is None:
                continue

            _, labels, retrain = result

            if not np.any(labels == 1):
                continue

            # Match the detected outliers with the timestamps.
            outliers = [self.timestamp_buffer[i] for i, label in enumerate(labels) if label == 1]

            results.extend(outliers)

            # For research purposes, if there is a retrain, save the model. Also, it is used as
            # a way to save the model in case of a crash.
            if retrain:
                self._save_state(
                    f"models/{self.station_id}_{self.variable}_{self.window_size}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.pkl")

            self.timestamp_buffer = []

        return results if len(results) > 0 else None

    def _save_state(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

    def _load_model(self):
        files = list(filter(lambda file: file.startswith(f"{self.station_id}_{self.variable}"), os.listdir("models")))

        # If there is no model, create a new one.
        if len(files) <= 0:
            return MKWIForestBatchPipeline(
                score_threshold=SCORE_THRESHOLD,
                alpha=ALPHA,
                slope_threshold=SLOPE_THRESHOLD,
                window_size=self.window_size)

        if len(files) == 1:
            with open(f"models/{files[0]}", "rb") as f:
                self.window_size = int(files[0].split("_")[2])
                return pickle.load(f)

        # Load the most recent model.
        files.sort()
        with open(f"models/{files[-1]}", "rb") as f:
            self.window_size = int(files[0].split("_")[2])
            return pickle.load(f)
