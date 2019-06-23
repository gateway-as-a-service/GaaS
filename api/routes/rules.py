from flask.views import MethodView
from flask import request
from flask import jsonify

import api.server
from configs.config import HTTPStatusCodes
from services.rules_service import RulesService


class RulesView(MethodView):

    def __init__(self):
        self.rule_service = RulesService()

    def post(self):
        rule = request.get_json()
        rule_id = self.rule_service.create(rule)
        response = {
            "_id": str(rule_id),
        }

        return jsonify(response), HTTPStatusCodes.CREATED
