import os

from flask import Flask

from .config import config_by_name
from . import html_to_pdf, html_to_notion

def create_app(config_name):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app = Flask(__name__)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    app.config.from_object(config_by_name[config_name])
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    app.register_blueprint(html_to_pdf.html_to_pdf_bp)
    app.register_blueprint(html_to_notion.html_to_notions_bp)

    return app