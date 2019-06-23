import time

import api.server
import cherrypy

from configs.config import GATEWAY_SERVER_IP, GATEWAY_SERVER_PORT
from services.register_service import RegisterService

if __name__ == '__main__':
    cherrypy.tree.graft(api.server.app.wsgi_app, "/")
    cherrypy.config.update({
        "server.socket_host": GATEWAY_SERVER_IP,
        'server.socket_port': GATEWAY_SERVER_PORT,
        'engine.autoreload.on': False,
    })
    cherrypy.server.subscribe()
    cherrypy.engine.start()
    time.sleep(5)
    register_service = RegisterService(logger=api.server.app.logger)
    api.server.app.logger.debug(register_service.register_gateway())

    api.server.app.logger.debug("Server has started at {}:{}".format(GATEWAY_SERVER_IP, GATEWAY_SERVER_PORT))

    while True:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            break
