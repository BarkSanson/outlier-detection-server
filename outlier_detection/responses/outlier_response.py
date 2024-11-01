from itertools import chain

from outlier_detection.station_outlier_detector import OutliersDetected


class OutlierResponse:
    def __init__(self):
        self.outliers_detected: list[OutliersDetected] = []

    def add_detection(self, detection: OutliersDetected):
        self.outliers_detected.append(detection)

    def to_json(self):
        return list(chain.from_iterable([outlier.to_json() for outlier in self.outliers_detected]))

    def __len__(self):
        return len(self.outliers_detected)