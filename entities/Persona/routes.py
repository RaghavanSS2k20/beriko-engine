from flask import Blueprint, request, jsonify
import json

persona_route = Blueprint("persona",__name__)
from .model import Persona
from .service import handle_create_persona, handle_update_persona
from utils.send_response import send_response

@persona_route.route("/", methods=['POST', 'PATCH'])
def update_user():
    data = request.json  # Get JSON data
    user_id = data["user_id"]
    if not user_id:
        send_response(status_code=400, success=False, message="User_id required")

    try:
        if request.method == 'POST':
            # Create new persona
            
            persona = handle_create_persona(user_id)
            return send_response(success=True, data=persona.to_json(), message="Persona created successfully")
        elif request.method == 'PATCH':
            # Update existing persona
            persona = handle_update_persona(user_id)
            return send_response(success=True, data=persona, message="Persona updated successfully")
    except Exception as e:
        print(e)
        return send_response(success=False, error=str(e), message="Error while processing persona", status_code=500)
    


@persona_route.get("/")
def get_persona():
    
    try:
        # Fetch all persona objects
        personas = Persona.objects()  # Returns a QuerySet of all documents
        # Convert to JSON-friendly format
        result = [
            {
                "id": str(p.id),
                "charecter_persona": p.charecter_persona,
                "user_id": p.user_id
            } 
            for p in personas
        ]
        return jsonify({"success": True, "data": result, "message": "All personas fetched successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "message": "Error fetching personas"}), 500

