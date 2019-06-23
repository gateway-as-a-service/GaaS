import os
import uuid

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
SCRIPTS_FOLDER = os.path.join(PROJECT_ROOT, "scripts")
LOGS_FOLDER = os.path.join(PROJECT_ROOT, "logs")
if not os.path.exists(LOGS_FOLDER):
    os.mkdir(LOGS_FOLDER)

NGROK_PATH = os.path.join(SCRIPTS_FOLDER, "ngrok.exe")
# if not os.path.exists(NGROK_PATH):
# raise Exception("Ngrok wasn't found")

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6968
SERVER_ADDRESS = "{}:{}".format(SERVER_IP, SERVER_PORT)

GATEWAY_UUID = "e1799142-0430-48f4-9b5d-1348591c0bf7"
GATEWAY_NAME = "First Gateway"
GATEWAY_DESCRIPTION = "First gateway description"

GATEWAY_SERVER_NAME = "GATEWAY_SERVER"
GATEWAY_SERVER_IP = "0.0.0.0"
GATEWAY_SERVER_PORT = 6001
GATEWAY_SERVER_URL = "{}:{}".format(GATEWAY_SERVER_IP, GATEWAY_SERVER_PORT)

USE_PRODUCTION_SERVER = True
if USE_PRODUCTION_SERVER:
    GASS_SERVER_IP = "18.203.185.40"
    GASS_SERVER_PORT = 80
    GASS_SERVER_API_VERSION = "v1"
    GASS_SERVER_API_URL = "http://{}:{}/api/{}".format(GASS_SERVER_IP, GASS_SERVER_PORT, GASS_SERVER_API_VERSION)
else:
    GASS_SERVER_IP = "http://127.0.0.1"
    GASS_SERVER_PORT = 6000
    GASS_SERVER_API_VERSION = "v1"
    GASS_SERVER_API_URL = "{}:{}/api/{}".format(GASS_SERVER_IP, GASS_SERVER_PORT, GASS_SERVER_API_VERSION)

GASS_REDIS_HOSTNAME = "127.0.0.1"
GASS_REDIS_PORT = 6379

GASS_REDIS_DOCKET_CONTAINERS_PROTOCOLS_HASH_KEY = "docker_protocols_containers"

# MQTT Broker Config
MQTT_BROKER_ADDRESS = "127.0.0.1"

# Message Forward
MESSAGE_FORWARD_REDIS_PUBSUB = "command_message_forward"

# Processor Pub-Sub Channel
REDIS_PUBSUB_DEVICES_MESSAGE_CHANNEL = "devices_messages"


class HTTPStatusCodes(object):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409

    INTERNAL_SERVER_ERROR = 500
