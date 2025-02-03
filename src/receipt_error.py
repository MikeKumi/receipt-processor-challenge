class ReceiptError(Exception):
    def __init__(self, message, error_type, description):
        super().__init__(message)
        self.error_type = error_type
        self.description = description
