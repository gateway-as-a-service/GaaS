import docker
import docker.errors

from configs.config import GASS_REDIS_PORT, GASS_REDIS_HOSTNAME, GASS_REDIS_DOCKET_CONTAINERS_PROTOCOLS_HASH_KEY
from discovery.libs.utils import FakeLogger


class DockerService(object):

    def __init__(self, logger):
        self.logger = logger

        self.docker_client = docker.from_env()

    def start_coap_microservice(self):
        container = self.docker_client.containers.run(
            "gass/coap_forward", auto_remove=True, ports={"5683/udp": 5682}, name="coap-microservice",
            detach=True
        )
        self.logger.info("Started container {} for image gass/coap_forward".format(container.id))
        return container.id

    def start_mqtt_broker(self):
        container = self.docker_client.containers.run(
            "eclipse-mosquitto", auto_remove=True, ports={"1883": 1883, "9883": 9883}, name='mqtt-broker',
            detach=True
        )
        self.logger.info("Started container {} for image eclipse-mosquitto".format(container.id))
        return container.id

    def start_mqtt_microservice(self):
        container = self.docker_client.containers.run(
            "gass/mqtt_forward", auto_remove=True, name="mqtt-microservice", detach=True,
        )
        self.logger.info("Started container {} for image gass/mqtt_forward".format(container.id))
        return container.id

    def get_containers(self):
        return self.docker_client.containers.list()

    def get_container(self, id):
        try:
            return self.docker_client.containers.get(id)
        except docker.errors.NotFound as err:
            self.logger.error(
                "Container {} doesn't exist. Reason: {}".format(id, err)
            )
            return None
        except Exception as err:
            self.logger.error(
                "Some error occurred during the retrieve of container with id: {}. Reason: {}"
                    .format(id, err)
            )
            raise err

    def kill_all(self):
        # Before starting the discovery service, kill all the containers and store those
        # that have been killed to be re-spawn again

        killed_images = set()
        for container in self.docker_client.containers.list():
            container.kill()
            killed_images.add(container.image)

            self.logger.info(
                "Killed container. Id: {}. Name: {}, Image: {}"
                    .format(container.id, container.name, container.image)
            )

        return killed_images

    def kill(self, id):
        self.docker_client.containers.get(id).kill()


if __name__ == '__main__':
    import walrus

    walrus = walrus.Database(host=GASS_REDIS_HOSTNAME, port=GASS_REDIS_PORT)
    docker_container_protocol = walrus.Hash(key=GASS_REDIS_DOCKET_CONTAINERS_PROTOCOLS_HASH_KEY)

    docker_service = DockerService(FakeLogger())

    # mqtt_container_id = docker_service.start_mqtt_microservice()
    # print(mqtt_container_id)
    # docker_container_protocol["MQTT"] = mqtt_container_id

    # docker_service.kill("ef2178a090be7d785680cf34bfc913c9ec397c9a185ac2403d962e9ba1f6ab39")
