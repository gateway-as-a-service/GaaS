import time

from docker.errors import NotFound

from configs.config import GASS_REDIS_HOSTNAME, GASS_REDIS_PORT, GASS_REDIS_DOCKET_CONTAINERS_PROTOCOLS_HASH_KEY
from discovery.libs.utils import retrieve_logger
from services.docker_service import DockerService

import walrus


class DockerMonitor(object):
    SLEEP_PERIOD = 10

    CONTAINERS = ["MQTT", "COAP"]

    def __init__(self):
        self.logger = retrieve_logger("docker_monitor")
        self.docker_service = DockerService(self.logger)

        self.walrus = walrus.Database(host=GASS_REDIS_HOSTNAME, port=GASS_REDIS_PORT)
        self.docker_container_protocols = self.walrus.Hash(key=GASS_REDIS_DOCKET_CONTAINERS_PROTOCOLS_HASH_KEY)

        self.protocol_create = {
            "COAP": self.docker_service.start_coap_microservice,
            "MQTT": self.docker_service.start_mqtt_microservice,
        }

    def run(self):
        for container_protocol in self.CONTAINERS:
            if container_protocol not in self.docker_container_protocols:
                continue

            container_id = self.docker_container_protocols[container_protocol].decode("utf-8")
            try:
                container = self.docker_service.get_container(container_id)
                if container:
                    self.logger.info(
                        "Docker container for protocol {} with id {} is healthy"
                            .format(container_protocol, container_id)
                    )
                    continue

                self.logger.error("Docker container {} wasn't found".format(container_id))
                self.logger.info("Create container for protocol: {}".format(container_protocol))
                new_container_id = self.protocol_create[container_protocol]()
                self.docker_container_protocols[container_protocol] = new_container_id

            except Exception as err:
                self.logger.error(
                    "Some unexpected error occurred during the verification of status for container protocol: {}. "
                    "Reason: {}"
                        .format(container_protocol, err)
                )

    def start(self):
        self.logger.info("Starting monitoring the docker containers")

        while True:
            self.logger.info("Checking the state of the containers")

            try:
                self.run()
            except Exception as err:
                self.logger.error(
                    "Some error occurred during the verification of the containers. Reason: {}"
                        .format(err)
                )
            finally:
                self.logger.info("Sleeping..")
                time.sleep(self.SLEEP_PERIOD)


if __name__ == '__main__':
    docker_monitor = DockerMonitor()
    docker_monitor.start()
