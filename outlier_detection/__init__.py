import logging
import os

from flask import Flask


def configure_loggers():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    app_logger = logging.getLogger('app_logger')
    app_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("./logs/results.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    app_logger.addHandler(file_handler)

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs('models', exist_ok=True)

    configure_loggers()

    from outlier_detection.blueprints import detection
    app.register_blueprint(detection.bp)

    return app
