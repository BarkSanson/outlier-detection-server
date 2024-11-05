import logging
import os

import requests
from flask import Blueprint, request

from outlier_detection.requests import InitializeRequest
from outlier_detection.requests.detection_request import DetectionRequest
from outlier_detection.services.outlier_detection_service import detection_service

bp = Blueprint('detection', __name__)
app_logger = logging.getLogger('app_logger')

@bp.route('/initialize', methods=['POST'])
def initialize():
    station_data = InitializeRequest.from_json(request.json)

    detection_service.add_station(station_data)

    app_logger.info(f"Station {station_data.station_id} initialized with variables {station_data.variables}")

    return {"status": "Ok"}, 200

@bp.route('/detection', methods=['POST'])
def detection():
    app_logger.info(f"Received JSON {request.json}")
    detection_request = DetectionRequest.from_json(request.json)

    try:
        result = detection_service.detect_outliers(detection_request)
    except KeyError:
        app_logger.error(f"Station {detection_request.station_id} not initialized")

        return {"status": "Station not initialized"}, 404

    if result is None:
        app_logger.info("No outliers yet")

        return {"status": "Ok"}, 200

    #requests.post(
    #    f"{os.environ['DATA_SERVER_ENDPOINT']}",
    #    json=result.to_json())

    app_logger.info(f"{result.to_json()}")

    return {"status": "Outliers detected"}, 200
