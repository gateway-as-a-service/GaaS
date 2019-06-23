import redis
from flask import jsonify
from flask import request
from flask.views import MethodView

import api.server
from configs.config import HTTPStatusCodes
from forward.protocol_filter_handler import ProtocolFilterHandler
from receivers.config import REDIS_HOSTNAME, REDIS_PORT
from services.devices_services import DevicesService


class DevicesCommandView(MethodView):
    PATCH_REQUIRED_FIELDS = {"value"}

    def __init__(self):
        self.logger = api.server.app.logger
        self.devices_service = DevicesService(logger=self.logger)
        self.protocol_filter_handler = ProtocolFilterHandler(self.logger)

        self.redis_connection = redis.StrictRedis(REDIS_HOSTNAME, REDIS_PORT)
        self.redis_connection.pubsub()

    def _validate_patch_body(self, body):
        if not isinstance(body, dict):
            return "The body must be an object"

        missing_fields = self.PATCH_REQUIRED_FIELDS - body.keys()
        if missing_fields:
            return "Missing fields: {}".format(missing_fields)

    def patch(self, device_uuid):
        body = request.get_json()
        validation_error_message = self._validate_patch_body(body)
        if validation_error_message:
            self.logger.error(
                "Some error occurred during the validation of the body. Reason: {}".format(validation_error_message)
            )
            response = {
                "message": validation_error_message,
            }
            return jsonify(response), HTTPStatusCodes.BAD_REQUEST

        device_uuid = str(device_uuid)
        device = self.devices_service.find_by_device_id(device_uuid)
        if not device:
            self.logger.error("Device {} wasn't found".format(device_uuid))
            response = {
                "message": "Device not found",
            }
            return jsonify(response), HTTPStatusCodes.NOT_FOUND

        message = {
            "device_info": {
                "device_uuid": device["id"],
                "protocol": device["protocol"],
                "ip": device["ip"],
                "port": device.get("port", 0)
            },
            "value": body["value"],
        }
        self.protocol_filter_handler.parse(message)

        return jsonify({}), HTTPStatusCodes.NO_CONTENT
