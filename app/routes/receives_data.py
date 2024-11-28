from flask import request, jsonify
from app.service.device_service import handle_upsert
from app.service.interaction_service import create_relation_interaction
from app.routes.phone_route import phone_blueprint
from app.utills.functions_utills import get_models_from_data

@phone_blueprint.route("/phone_tracker", methods=['POST'])
def get_interaction():
   data = request.json
   devices, interaction = get_models_from_data(data)
   res_device = handle_upsert(devices)
   res_interaction = create_relation_interaction(data)
   return jsonify({"res_device":res_device, "res_interaction": res_interaction }), 201

