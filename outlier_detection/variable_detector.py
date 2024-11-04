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
        self.model = MKWIForestBatchPipeline(
            score_threshold=SCORE_THRESHOLD,
            alpha=ALPHA,
            slope_threshold=SLOPE_THRESHOLD,
            window_size=window_size)
        self.timestamp_buffer = []

    def update(self, data: dict) -> list | None:
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

            # For research purposes, if there is a retrain, save the model.
            if retrain:
                self.model.save_state(f"models/{self.station_id}_{self.variable}_{datetime.now().strftime("%Y%m%d-%H%M%S")}.pkl")

            self.timestamp_buffer = []

        return results if len(results) > 0 else None
