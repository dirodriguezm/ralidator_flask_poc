from flask import _request_ctx_stack
from ralidator.ralidator import Ralidator


class FlaskRalidator(object):
    def __init__(self, app=None):
        self.app = app
        self.filters_map = {}
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.filters_map = app.config["FILTERS_MAP"]

        @app.before_request
        def before_request():
            self.set_ralidator_on_context()

        @app.after_request
        def after_request(response):
            if response.status_code < 400:
                response.set_data(self.ralidator.apply_filters(response.get_json()))
            return response

    def set_ralidator_on_context(self):
        ctx = _request_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "ralidator"):
                ctx.ralidator = Ralidator(
                    self.filters_map, ctx.request.headers.get("token")
                )

    @property
    def ralidator(self):
        self.set_ralidator_on_context()
        ctx = _request_ctx_stack.top
        return ctx.ralidator


def set_filters_decorator(filter_list):
    def wrapper_decorator(arg_function):
        def decorator_function(*args, **kwargs):
            ctx = _request_ctx_stack.top
            ctx.ralidator.set_filters(filter_list)

            return arg_function(*args, **kwargs)

        return decorator_function

    return wrapper_decorator


def set_permissions_decorator(permissions_list):
    def wrapper_decorator(arg_function):
        def decorator_function(*args, **kwargs):
            ctx = _request_ctx_stack.top
            ctx.ralidator.set_permissions(permissions_list)

            return arg_function(*args, **kwargs)

        return decorator_function

    return wrapper_decorator


def check_permissions_decorator(arg_function):
    def decorator_function(*args, **kwargs):
        ctx = _request_ctx_stack.top
        if ctx.ralidator.check_allowed():
            return arg_function(*args, **kwargs)
        else:
            return "Forbidden", 403

    return decorator_function
