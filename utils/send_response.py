from flask import jsonify

def send_response(success=True, data=None, message=None, error=None, status_code=200):
    """
    Returns a standardized JSON response.
    
    - success: True/False
    - data: any payload (for success)
    - message: success message
    - error: error message/details
    - status_code: HTTP status code
    """
    if status_code == 400 or status_code == 500 :
            success = False
    if success:
        response = {
            "status": True,
            "data": data or {},
            "message": message or "Request successful"
        }
    else:
        response = {
            "status": "error",
            "error": error or "Something went wrong"
        }
        # Optional: override status code if not provided
        

    return jsonify(response), status_code
