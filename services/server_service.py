import requests

from configs.config import GATEWAY_UUID, HTTPStatusCodes, SERVER_ADDRESS
from discovery.libs.utils import FakeLogger


class ServerService(object):

    def __init__(self, *args, **kwargs):
        self.logger = kwargs.get("logger") or FakeLogger()

    def send_perform_actions(self, performed_actions):
        url = "{}/{}/actions".format(SERVER_ADDRESS, GATEWAY_UUID)
        body = performed_actions
        try:
            response = requests.post(url, json=body)
        except Exception as err:
            self.logger.error(
                "Failed to send the the server the performed actions. Reason: {}"
                    .format(err), exc_info=True
            )
            return False

        if not response:
            self.logger.error("Failed to retrieve the response from server")
            return False

        if response.status_code != HTTPStatusCodes.CREATED:
            self.logger.error(
                "Failed to register the performed actions. Status code: {}. Response: {}"
                    .format(response.status_code, response.text)
            )
            return False

        return True


if __name__ == '__main__':
    server_service = ServerService()
    server_service.send_perform_actions({})
