import json

from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP

from discovery.libs.utils import retrieve_logger
from receivers.handlers.receiver_handler import MessageReceiverHandler


class DevicesResource(Resource):
    REDIS_PUBSUB_DEVICES_MESSAGE_CHANNEL = "devices_messages"

    def __init__(self, name="DevicesResource"):
        super(DevicesResource, self).__init__(name)

        self.message_receiver_handler = MessageReceiverHandler()

        self.logger = retrieve_logger("device_message_receiver")

    def render_PUT(self, request):
        message = json.loads(request.payload)
        self.logger.info("Received message: {}".format(message))
        self.message_receiver_handler.send_message_to_processing(message)

        return self

    def render_GET(self, request):
        pass

    def render_GET_advanced(self, request, response):
        pass

    def render_PUT_advanced(self, request, response):
        pass

    def render_POST(self, request):
        pass

    def render_POST_advanced(self, request, response):
        pass

    def render_DELETE(self, request):
        pass

    def render_DELETE_advanced(self, request, response):
        pass


class CoAPServer(CoAP):
    def __init__(self, host, port, ):
        super().__init__((host, port))
        self.add_resource('devices/', DevicesResource())


def _start_server():
    server = CoAPServer("0.0.0.0", 5683)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Closing....")


if __name__ == '__main__':
    _start_server()
