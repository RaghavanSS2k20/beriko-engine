from flask import jsonify,Blueprint
from scripts.suggest_profiles import get_matching_for_profile
from utils.send_response import send_response
suggestions_module = Blueprint("suggestions",__name__)

@suggestions_module.route("/<user>", methods=['GET'])
def get_suggestions(user):
    try:
        results = get_matching_for_profile(user)
        return send_response(success=True, data=results, status_code=200)
    except Exception as e:
        return send_response(success=False,status_code=500, message="Error while getting matches", error=e)




