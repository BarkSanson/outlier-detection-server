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

    def update(self, request: DetectionRequest) -> OutlierResponse | None:
        results = OutlierResponse()

        for station_request in request.requests:
            if station_request.id_station not in self.stations:
                continue

            station = self.stations[station_request.id_station]
            result = station.update(station_request.variables)

            if result is not None:
                results.add_detection(result)

        if len(results) == 0:
            return None

        return results

detection_service = StationOutlierDetectionService()