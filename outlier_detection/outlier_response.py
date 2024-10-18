from dataclasses import dataclass


@dataclass
class VariableOutliers:
    type: str
    dates: list[str]

    def to_json(self):
        return {
            "type": self.type,
            "dates": self.dates
        }


class OutlierResponse:
    def __init__(self):
        self.outliers: list[VariableOutliers] = []

    def add_outlier(self, outliers: VariableOutliers):
        self.outliers.append(outliers)

    def __len__(self):
        return len(self.outliers)

    def to_json(self):
        return [outlier.to_json() for outlier in self.outliers]
