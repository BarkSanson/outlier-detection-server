import numpy as np
from sklearn.ensemble import IsolationForest

from online_outlier_detection.pipelines.base.batch_detector_pipeline import BatchDetectorPipeline
from online_outlier_detection.drift import MannKendallWilcoxonDriftDetector


class MKWIForestBatchPipeline(BatchDetectorPipeline):
    def __init__(self,
                 score_threshold: float,
                 alpha: float,
                 slope_threshold: float,
                 window_size: int):
        super().__init__(score_threshold, alpha, slope_threshold, window_size)
        self.model = IsolationForest()
        self.drift_detector = MannKendallWilcoxonDriftDetector(alpha, slope_threshold)

    def update(self, x) -> tuple[np.ndarray, np.ndarray, bool] | None:
        """
        Update the pipeline with a new data point.
        :param x: The new data point.
        :return: If the pipeline has detected a drift, it will return the scores and labels of the reference
        window, and a boolean indicating that a drift has occurred. If no drift has occurred, the pipeline will return
        the scores and labels of the current window, and a boolean indicating that no drift has occurred.
        """
        self.window.append(x)

        if not self.window.is_full():
            return None

        if not self.warm:
            scores, labels = self._first_training()
            return scores, labels, True

        if self.drift_detector.detect_drift(self.window.get(), self.reference_window):
            self._retrain()

            scores = np.abs(self.model.score_samples(self.reference_window.reshape(-1, 1)))
            labels = np.where(scores > self.score_threshold, 1, 0)

            self.window.clear()
            return scores, labels, True

        scores = np.abs(self.model.score_samples(self.window.get().reshape(-1, 1)))
        labels = np.where(scores > self.score_threshold, 1, 0)

        self.window.clear()
        return scores, labels, False
