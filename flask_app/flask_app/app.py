from flask import Flask
from flask_ralidator.flask_ralidator import (
    set_filters_decorator,
    set_permissions_decorator,
    check_permissions_decorator,
)


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    print(app.config)

    from flask_app.extensions import ralidator

    ralidator.init_app(app)

    return app


app = create_app("settings")


@app.route("/")
@set_permissions_decorator(["permission1"])
@check_permissions_decorator
@set_filters_decorator(["filter1", "filter2"])
def hello_world():
    return {"json": False}


app.run()
