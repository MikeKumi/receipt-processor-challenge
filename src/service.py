"""
This module activates the Flask server, logger, and endpoints for receipt point processing and retrieving. 

Functions include:
- process_receipt_json: Starts receipt processing by validating the json against the schema, creating the Receipt object, and then calculating the points necessary.
- _validate_json: Validate that json input matches the receipt schema
- Functions for retrieving points based on receipt data: [
    _get_retailer_points, 
    _get_total_points, 
    _get_purchase_date_points, 
    _get_purchase_time_points, 
    _get_items_points, 
    _get_item_points
]

Test:   tests.service.py
Author: Michael Kumicich
Date:   February 4, 2025
"""


import math

from datetime import datetime
from jsonschema import validate, ValidationError
from schemas.receipt_schema import receipt_schema
from receipt_error import ReceiptError
from receipt_data import Receipt


def process_receipt_json(json_dict):
    """
    
    """
    _validate_json(json_dict)
    receipt = Receipt(json_dict)
    points = 0

    points += _get_retailer_points(receipt)
    points += _get_total_points(receipt)
    points += _get_purchase_date_points(receipt)
    points += _get_purchase_time_points(receipt)
    points += _get_items_points(receipt)

    return points

def _get_retailer_points(receipt):
    points = 0
    for letter in receipt.retailer:
        if letter.isalnum():
            points += 1

    return points

def _get_total_points(receipt):
    points = 0
    print(str(receipt.total))
    if str(receipt.total).endswith(".0"):
        points += 50

    total = receipt.total
    if total % 0.25 == 0:
        points += 25

    return points

def _get_purchase_date_points(receipt):
    receipt_date = datetime.strptime(receipt.purchase_date, "%Y-%m-%d")
    return 6 if receipt_date.day % 2 == 1 else 0

def _get_purchase_time_points(receipt):
    receipt_time = datetime.strptime(receipt.purchase_time, "%H:%M").time()  # Convert to time object
    time_2pm = datetime.strptime("14:00", "%H:%M").time()
    time_4pm = datetime.strptime("16:00", "%H:%M").time()

    return 10 if receipt_time > time_2pm and receipt_time < time_4pm else 0

def _get_items_points(receipt):
    points = 0
    points += (len(receipt.items) // 2) * 5 

    for item in receipt.items:
        points += _get_item_points(item)

    return points

def _get_item_points(item):
    trimmed_description = item.short_description.strip()
    if len(trimmed_description) % 3 == 0:
        return math.ceil(item.price * 0.2)
    else:
        return 0

def _validate_json(json_dict):
    try:
        validate(json_dict, receipt_schema)
    except ValidationError as e:
        raise ReceiptError(
            message=e.message, 
            error_type=400, 
            description="The receipt is invalid."
        )
