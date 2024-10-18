import logging
import os

from flask import Flask, request

from .detection_wrapper import DetectionWrapper
from .station_data import StationData


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app_logger = logging.getLogger('app_logger')
    app_logger.setLevel(logging.INFO)

    handler = logging.FileHandler("results.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    app_logger.addHandler(handler)

    wrapper = DetectionWrapper()

    @app.route('/detection')
    def data():
        station_values = StationData.from_json(request.json)

        result = wrapper.update(station_values)

        # TODO: send results to the other server
        # - DATA_SERVER_HOST
        # - DATA_SERVER_PORT
        # - DATA_SERVER_ENDPOINT
        if result is None:
            app_logger.info("No outliers yet")

            return {"status": "Ok"}, 200

        app_logger.info(f"{result.to_json()}")

        return result.to_json(), 200

    return app
