from flask import Blueprint, request, jsonify
import json
from .service import get_user_insights, get_persona_for_user

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

@persona_route.get("/<user_id>")
def get_persona_route(user_id):
    try:
        # ✅ Fetch persona using existing service
        res = get_persona_for_user(user_id)

        # ✅ If error inside service
        if not res.get("success"):
            return send_response(
                success=False,
                message=res.get("message", "Failed to fetch persona"),
                error=res.get("error"),
                status_code=404 if "not found" in res.get("message", "").lower() else 400,
            )

        # ✅ Success — send persona data
        return send_response(
            success=True,
            data=res.get("data"),
            message=res.get("message", "Persona fetched successfully"),
        )

    except Exception as e:
        # ✅ Catch route-level exceptions
        return send_response(
            success=False,
            error=str(e),
            message="Error while processing persona",
            status_code=500,
        )

@persona_route.get("/insights/<user_id>")
def get_insigths(user_id):
    res = get_user_insights(user_id)
    if res["success"]:
        return send_response(success=True,
            data=res["data"]
        )
    else:
        return send_response(success=False,
            error=res["error"]
        )

