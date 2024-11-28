from flask import Blueprint
from app.repository.phone_repository import find_bluetooth_connections, \
    find_strong_signal_connections, count_connected_devices, is_connected, fetch_most_recent_interaction
from flask import Flask, request, jsonify

phone_blueprint = Blueprint("phone", __name__)

@phone_blueprint.route("/bluetooth", methods=['GET'])
def get_bluetooth_connections():
    connections = find_bluetooth_connections()
    return jsonify(connections), 200

@phone_blueprint.route("/strong-signal", methods=['GET'])
def get_strong_signal_connections():
    connections = find_strong_signal_connections()
    return jsonify(connections), 200


@phone_blueprint.route("/<device_id>/connected_count", methods=["GET"])
def get_connected_device_count(device_id):
    try:
        connected_count = count_connected_devices(device_id)
        return jsonify({
            "device_id": device_id,
            "connected_count": connected_count
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@phone_blueprint.route("/connection", methods=["GET"])
def check_device_connection():
    device_id_1 = request.args.get("device_id_1")
    device_id_2 = request.args.get("device_id_2")

    if not device_id_1 or not device_id_2:
        return jsonify({"error": "Both device_id_1 and device_id_2 are required"}), 400

    try:
        connected = is_connected(device_id_1, device_id_2)
        return jsonify({
            "device_id_1": device_id_1,
            "device_id_2": device_id_2,
            "is_connected": connected
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@phone_blueprint.route("/<device_id>/recent_interaction", methods=["GET"])
def get_recent_interaction(device_id):
    try:
        recent_interaction = fetch_most_recent_interaction(device_id)
        if recent_interaction:
            return jsonify({
                "device_id": device_id,
                "recent_interaction": recent_interaction
            }), 200
        else:
            return jsonify({
                "device_id": device_id,
                "message": "No interactions found for this device."
            }), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
