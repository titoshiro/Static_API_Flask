import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    if members is not None:
        return jsonify(members), 200
    else:
        return jsonify({"error": "Not found"}), 404
    

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is not None:
        return jsonify(member), 200
    else:
        return jsonify({"message": "Member not found"}), 404

@app.route('/member', methods=['POST'])
def add_member():
    data = request.get_json()

    if data is None or "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"error": "Bad request"}), 400

    if "id" not in data:
        data["id"] = None

    jackson_family.add_member(data)
    return jsonify(), 200

@app.route('/member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.get_json()
    if jackson_family.update_member(member_id, data):
        return jsonify(), 200
    else:
        return jsonify({"error": "Not found"}), 404

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
