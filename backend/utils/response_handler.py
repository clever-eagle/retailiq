from flask import jsonify
from datetime import datetime


class ResponseHandler:
    """
    Standardized response handler for API endpoints
    """

    @staticmethod
    def success(data, message="Success", status_code=200):
        """
        Create a successful response
        """
        response = {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
        return jsonify(response), status_code

    @staticmethod
    def error(message, status_code=400, error_details=None):
        """
        Create an error response
        """
        response = {
            "success": False,
            "message": message,
            "error": error_details,
            "timestamp": datetime.now().isoformat(),
        }
        return jsonify(response), status_code

    @staticmethod
    def validation_error(field_errors):
        """
        Create a validation error response
        """
        response = {
            "success": False,
            "message": "Validation failed",
            "errors": field_errors,
            "timestamp": datetime.now().isoformat(),
        }
        return jsonify(response), 422

    @staticmethod
    def not_found(resource="Resource"):
        """
        Create a not found response
        """
        response = {
            "success": False,
            "message": f"{resource} not found",
            "timestamp": datetime.now().isoformat(),
        }
        return jsonify(response), 404

    @staticmethod
    def internal_error(message="Internal server error"):
        """
        Create an internal server error response
        """
        response = {
            "success": False,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }
        return jsonify(response), 500
