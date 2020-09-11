from flask_api import status


def handlePolling(id):

    # Incase not ready
    response = {"error_id": "task pending", "error_message": "video annotation task is being processed."}
    return response, status.HTTP_401_UNAUTHORIZED

    # # Incase not ready
    # response = {"error_id": "slow down", "error_message": "too faster api calls. Intervals incremented"}
    # return response, status.HTTP_401_UNAUTHORIZED
