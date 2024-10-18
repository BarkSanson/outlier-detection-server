import os

from flask import Flask, request

from .detection_wrapper import DetectionWrapper
from .station_data import StationData


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_pyfile('config.py')

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
            return {"status": "Ok"}, 200

        return result.to_json(), 200

    return app
