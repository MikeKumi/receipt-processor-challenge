receipt_schema = {
    "type": "object",
    "properties": {
        "retailer": {
            "description": "The name of the retailer or store the receipt is from.",
            "type": "string",
            "pattern": r"^[\\w\\s\\-&]+$"
        },
        "purchaseDate": {
            "description": "The date of the purchase printed on the receipt.",
            "type": "string", 
            "format": "date"
        },
        "purchaseTime": {
            "description": "The time of the purchase printed on the receipt. 24-hour time expected.",
            "type": "string", 
            "format": "time"
        },
        "total": {
            "description": "The total amount paid on the receipt.",
            "type": "string",
            "pattern": r"^\\d+\\.\\d{2}$"
        },
        "items": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "shortDescription": {
                        "description": "The Short Product Description for the item.",
                        "type": "string",
                        "pattern": r"^[\\w\\s\\-]+$"
                    },
                    "price": {
                        "description": "The total price payed for this item.",
                        "type": "string", 
                        "pattern": r"^\\d+\\.\\d{2}$"
                    }
                },
                "required": ["shortDescription", "price"],
                "additionalProperties": False
            }
        }
    },
    "required": ["retailer", "purchaseDate", "purchaseTime", "total", "items"],
    "additionalProperties": False
}