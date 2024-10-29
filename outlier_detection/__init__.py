import logging
import os

import requests
from flask import Flask, request

from .detection_wrapper import DetectionWrapper
from .station_data import StationData


def configure_logger():
    os.makedirs("logs", exist_ok=True)

    app_logger = logging.getLogger('app_logger')
    app_logger.setLevel(logging.INFO)

    handler = logging.FileHandler("./logs/results.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    app_logger.addHandler(handler)

    return app_logger


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs('data', exist_ok=True)

    wrapper = DetectionWrapper()

    app_logger = configure_logger()

    @app.post('/detection')
    def data():
        station_values = StationData.from_json(request.json)
        app_logger.info(f"Received JSON {request.json}")
        app_logger.info(f"Received data {station_values}")

        result = wrapper.update(station_values)

        if result is None:
            app_logger.info("No outliers yet")

            return {"status": "Ok"}, 200

        requests.post(
            f"{os.environ['DATA_SERVER_ENDPOINT']}",
            json=result.to_json())

        app_logger.info(f"{result.to_json()}")

        return {"status": "Outliers detected"}, 200

    return app
