"""
This module activates the Flask server, logger, and endpoints for receipt point processing and retrieving. 

Functions include:
- process_receipt: Starts receipt processing service at service.py
- get_receipt_points: Retrieves the amount of points for receipt from in-memory dictionary
- handle_error: Called in the instance of an error with processing the receipt JSON or for retrieving it. Sends a 400/404 code back to user.

Test:   tests.server.py
Author: Michael Kumicich
Date:   February 4, 2025
"""

import uuid
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
from service import process_receipt_json
from receipt_error import ReceiptError

app = Flask(__name__)

receipts = {}

# Create Rotating file logger that can store up to 1MB per file before creating a new one. Max number of files is 5 
handler = RotatingFileHandler('app.log', maxBytes=1_000_000, backupCount=5)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@app.route("/receipts/process", methods=['POST'])
def process_receipt():
    """
    POST: Endpoint to start receipt processing service and store the amount of points from it. 

    Returns:
        JSON with id for the processed receipt, which contains the key for retrieving the amount of points. 
    """
    logger.info("Received POST request to process receipt")
    uid = str(uuid.uuid4())
    json_dict = request.get_json()
    receipts[uid] = process_receipt_json(json_dict)
    return {"id": uid}

@app.route("/receipts/<string:id>/points", methods=['GET'])
def get_receipt_points(id):
    """
    GET: Endpoint to retrieve the number of points for a given receipt ID from process endpoint.

    Args:
        id: Receipt point key for receipts dictionary

    Returns: 
        JSON with the number of points for the given receipt ID
    """
    logger.info(f"Received GET request to retrieve points for receipt with ID: {id}")
    try:
        return {"points": receipts[id]}
    except KeyError as e:
        raise ReceiptError(
            message=e.message, 
            error_type=404, 
            description="No receipt found for that ID."
        )
    
@app.errorhandler(ReceiptError)
def handle_error(e):
    """
    Error handler for receipt errors. Returns error with status code and description back to client. 
    """
    logger.warning(e.message)
    response = jsonify({"error": e.error_type, "description": e.description})
    response.status_code = e.status_code
    return response


if __name__ == '__main__':
    app.run(debug=False)
