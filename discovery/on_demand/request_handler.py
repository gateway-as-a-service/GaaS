import json
import socket
import threading

from configs.config import GATEWAY_UUID, GASS_REDIS_HOSTNAME, GASS_REDIS_PORT, \
    GASS_REDIS_DOCKET_CONTAINERS_PROTOCOLS_HASH_KEY
from services.devices_services import DevicesService
from services.docker_service import DockerService
from services.register_service import RegisterService

import walrus


class ClientRequestHandler(threading.Thread):
    REQUIRED_FIELDS = {"id", "type", "name", "protocol", "ip"}

    MAX_ATTEMPTS_CONTAINER_PROTOCOL_START = 10

    def __init__(self, device_info, address, logger):
        super().__init__(daemon=True)
        self.device_info = self._transform_sen_ml_to_json(device_info)
        self.address = address
        self.logger = logger
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.devices_service = DevicesService(logger=self.logger)
        self.register_service = RegisterService(logger=self.logger)
        self.docker_service = DockerService(logger=self.logger)

        self.walrus = walrus.Database(host=GASS_REDIS_HOSTNAME, port=GASS_REDIS_PORT)
        self.containers_status = self.walrus.Hash(GASS_REDIS_DOCKET_CONTAINERS_PROTOCOLS_HASH_KEY)

        self.protocol_create = {
            "COAP": self._start_coap_microservice,
            "MQTT": self._start_mqtt_microservice,
        }
        self.protocol_check = {
            "COAP": self._verify_coap_microservice,
            "MQTT": self._verify_mqtt_microservices,
        }

    def _transform_sen_ml_to_json(self, data):
        device_info = json.loads(data.decode("utf-8"))
        if device_info.get("bver"):
            device_info.pop("bver")

        name = device_info.pop("n", None)
        if name:
            device_info["name"] = name

        value = device_info.pop("v", None)
        if value:
            device_info["value"] = value

        return device_info

    def _validate_request_message(self):
        missing_fields = self.REQUIRED_FIELDS - self.device_info.keys()
        if missing_fields:
            return "The request {} has some missing fields: {}".format(self.device_info, missing_fields)

    def _verify_mqtt_microservices(self):
        if "MQTT" not in self.containers_status:
            return False

        if "MQTT-BROKER" not in self.containers_status:
            return False

        return True

    def _verify_coap_microservice(self):
        return "COAP" in self.containers_status

    def _start_mqtt_microservice(self):
        if "MQTT-BROKER" not in self.containers_status:
            mqtt_broker_container_id = self.docker_service.start_mqtt_broker()
            self.containers_status["MQTT-BROKER"] = mqtt_broker_container_id
            self.logger.info("Start MQTT-BROKER container with id {}".format(mqtt_broker_container_id))

        if "MQTT" not in self.containers_status:
            mqtt_microservice_container_id = self.docker_service.start_mqtt_microservice()
            self.containers_status["MQTT"] = mqtt_microservice_container_id
            self.logger.info("Start MQTT container with id {}".format(mqtt_microservice_container_id))

    def _start_coap_microservice(self):
        coap_microservice_container_id = self.docker_service.start_coap_microservice()
        self.containers_status["COAP"] = coap_microservice_container_id
        self.logger.info("Start COAP container with id {}".format(coap_microservice_container_id))

    def _verify_container(self):
        protocol = self.device_info["protocol"]
        microservices_already_up = self.protocol_check[protocol]()
        if microservices_already_up:
            self.logger.info("There is a container for protocol: {}".format(protocol))
            return

        attempt = 0
        while attempt < self.MAX_ATTEMPTS_CONTAINER_PROTOCOL_START:

            try:
                self.logger.info("No docker for protocol: {}. Starting the microservice".format(protocol))
                self.logger.info("Attempt : {}".format(attempt))
                self.protocol_create[protocol]()

                break

            except Exception as err:
                self.logger.error(
                    "Some error occurred while the start of the microservice for protocol {} . Reason: {}"
                        .format(protocol, err), exc_info=True
                )
                attempt += 1

    def run(self):
        self.logger.debug("Received register response: {} ---- from {}".format(self.device_info, self.address))
        error_validation_message = self._validate_request_message()
        if error_validation_message:
            self.logger.error(error_validation_message)
            self.sock.sendto(b"MISSING FIELDS", self.address)
            self.sock.close()
            return

        self.device_info["gateway_uuid"] = GATEWAY_UUID
        devices_has_been_register = self.register_service.register_device(self.device_info)
        if not devices_has_been_register:
            self.logger.critical("Failed to register the device to GaSS Server")
            self.sock.sendto(b"Failed to register because the GaSS server is unreachable", self.address)
            self.sock.close()
            return

        device = self.devices_service.find_by_device_id(self.device_info["id"])
        if device:
            self.logger.debug("Device {} has been already registered".format(self.device_info["id"]))

            self._verify_container()

            self.sock.sendto(b"OK", self.address)
            self.sock.close()
            return

        device = self.devices_service.create(dict(self.device_info))
        if not device:
            self.logger.error("Failed to create the device")
            self.sock.sendto(b"FAILED TO REGISTER", self.address)
            self.sock.close()
            return

        # Start the micro-service
        # Check in microservice is on or not
        # If it will create the microservice, store the container id into REDIS
        # So, the monitor will be able to check which container is still alive
        # And if it finds that some containers doesn't exists will create another one

        self._verify_container()

        try:
            self.logger.debug("Send ACK to device at address: {}: {}".format(self.address[0], self.address[1]))
        except Exception as err:
            print(err)
            raise
        self.sock.sendto(b"OK", self.address)
        self.sock.close()

        self.logger.debug("Devices has been registered")
        self.logger.debug("Sent registering confirmation")


if __name__ == '__main__':
    import docker

    client = docker.from_env()
    print([(container.id, container.name) for container in client.containers.list(filters={'status': 'running'})])
    # docker run - -rm - p 5682: 5683 / udp     gass / coap_forward
    # container = client.containers.run("gass/coap_forward", auto_remove=True, ports={"5683/udp": 5682}, detach=True)
    #
    # count = 0
    # while count < 100:
    #     time.sleep(2)
    #     print(container.logs().decode("utf-8"))
    #     count += 1
    #
    # container.kill()
