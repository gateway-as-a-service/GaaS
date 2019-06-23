import flask

from api.libs.utils import register_logger
from api.routes.devices import DevicesCommandView
from api.routes.rules import RulesView
from configs.config import GATEWAY_SERVER_NAME, GATEWAY_SERVER_IP, GATEWAY_SERVER_PORT

app = flask.Flask(GATEWAY_SERVER_NAME)
register_logger(app)

devices_command_view = DevicesCommandView.as_view("DevicesCommandView")
rules_view = RulesView.as_view("RulesView")

app.add_url_rule(
    rule="/api/devices/<uuid:device_uuid>",
    view_func=devices_command_view,
    methods=["PATCH", ]
)

app.add_url_rule(
    rule='/api/rules',
    view_func=rules_view,
    methods=["POST", ]
)

if __name__ == '__main__':
    app.run(GATEWAY_SERVER_IP, GATEWAY_SERVER_PORT, True)
