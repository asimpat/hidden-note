from rest_framework.response import Response
from rest_framework import status


def error_response(message, code="invalid_request", status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }, status=status_code)
