from outlier_detection.requests import DetectionRequest
from outlier_detection.responses import OutlierResponse
from outlier_detection.requests import InitializeRequest
from outlier_detection.station_outlier_detector import StationOutlierDetector

class StationOutlierDetectionService:
    def __init__(self):
        self.stations = {}

    def add_station(self, initialize_request: InitializeRequest):
        self.stations[initialize_request.station_id] = StationOutlierDetector(
            station_id=initialize_request.station_id,
            variables=initialize_request.variables)

    def detect_outliers(self, request: DetectionRequest) -> OutlierResponse | None:
        results = OutlierResponse()

        samples = self._transform_samples(request.samples)

        result = self.stations[request.station_id].update(samples)

        if result is None:
            return None

        results.add_detection(result)

        return results

    def _transform_samples(self, samples):
        # Transform samples with shape:
        # {
        #   "mostres": [
        #       {
        #           "timestamp": "2021-09-01T00:00:00",
        #           "variable_1": 0.1,
        #           "variable_2": 0.2
        #       },
        #       {
        #           "timestamp": "2021-09-01T00:00:01",
        #           "variable_1": 0.2,
        #           "variable_2": 0.3
        #       }
        #   ]
        # }
        # to:
        # {
        #   "variable_1": {
        #       "data": [0.1, 0.2],
        #       "dates": ["2021-09-01T00:00:00", "2021-09-01T00:00:01"]
        #   },
        #   "variable_2": {
        #       "data": [0.2, 0.3],
        #       "dates": ["2021-09-01T00:00:00", "2021-09-01T00:00:01"]
        #   }
        # }
        transformed_data = {}

        for sample in samples:
            for variable, x in sample.items():
                if variable == "timestamp":
                    continue

                if variable not in transformed_data:
                    transformed_data[variable] = {"data": [], "dates": []}

                transformed_data[variable]["data"].append(x)
                transformed_data[variable]["dates"].append(sample["timestamp"])

        return transformed_data



detection_service = StationOutlierDetectionService()