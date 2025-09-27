from flask import Blueprint
from flask import request

trait_route = Blueprint("trait",__name__)
from .model import Trait
from .service import *
from utils.send_response import send_response

@trait_route.route("/update",methods = ['PUT'])
def update_traits():
    request_data = request.json
    print(request_data)
    user_id = request_data["user_id"]
    res = handle_update_traits(user_id,request_data["weights"])
    if res["success"]:
        return send_response(status_code=200, success=True, data=res["data"])
    else:
        return send_response(status_code=500, success=True, data=res["error"])