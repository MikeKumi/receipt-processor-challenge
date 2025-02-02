from flask import Flask, jsonify
from jsonschema import validate, ValidationError
import uuid

app = Flask(__name__)

receipts = {}

@app.route("/receipts/process", methods=['POST'])
def process_receipt():
    uid = str(uuid.uuid4())
    receipts[uid] = 10000
    return {"id": uid}

@app.route("/receipts/<string:id>/points", methods=['GET'])
def get_receipt_points(id):
    return {"points": receipts[id]}
    
@app.errorhandler(ValidationError)
def handle_validation_error(e):
    response = jsonify({"error": "BadRequest", "description": "No receipt found for that ID."})
    response.status_code = 400  # Bad Request
    return response


if __name__ == '__main__':
    app.run(debug=True)
