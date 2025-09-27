from utils.send_response import send_response
from .model import Trait, Variable
from ..Persona.service import handle_update_persona,update_interests
from scripts.update_weights import update_variable_weights
from mongoengine import DoesNotExist
from templates.template import *
from slugify import slugify

CHARECTER_TRAITS = ('behavioral', 'psychological', 'demographic')
  



# def update_traits(user_id, trait_type, variables):
#     """
#     Update or add variables for a user's trait.
    
#     Args:
#         user_id: str, the user's ID
#         trait_type: str, one of 'behavioral', 'psychological', 'demographic'
#         variables: list of dicts, e.g. [{"slug": "humour", "value": 0.9, "name": "Humour"}]
#     """
#     if trait_type not in CHARECTER_TRAITS:
#         return send_response(success=False, error="Invalid Character type", status_code=400)
    
#     try:
#         trait = Trait.objects.get(user_id=user_id, type=trait_type)
#     except DoesNotExist:
#         # Create a new trait document if it doesn't exist
#        return send_response(success=False,error="Trait Not yet created", status_code=500)

#     try:
    
#         # Create a map for quick lookup of existing variables
#         variable_map = {v.slug: v for v in trait.variables}
#         variables = update_variable_weights(trait.variables,variables)
#         for var in variables:
#             slug = var.get("slug")
#             value = var.get("value")
#             name = var.get("name", slug)
            
#             if slug in variable_map:
#                 # Update existing variable
#                 variable_map[slug].value = value
#                 variable_map[slug].name = name
#             else:
#                 # Add new variable
#                 trait.variables.append(Variable(slug=slug, name=name, value=value))
        
#         trait.save()
#         handle_update_persona(user_id)
#     except Exception as e:
#         print("error while updating the traits: ", e)
#         return send_response(success=False, error=e, message="error while updating the traits: ")
    
#     # Optional: return updated trait in JSON-friendly format
#     result = [
#         {"slug": v.slug, "name": v.name, "value": v.value} 
#         for v in trait.variables
#     ]
    
#     return send_response(data={"variables": result}, message="Trait updated successfully")

def update_traits(user_id, trait_type, variables):
    if trait_type not in CHARECTER_TRAITS:
        return {"success": False, "error": "Invalid Character type"}

    try:
        trait = Trait.objects.get(user_id=user_id, type=trait_type)
    except DoesNotExist:
        return {"success": False, "error": f"Trait {trait_type} not yet created"}

    try:
        # Convert existing variables into dicts
        existing_vars = [
            {"slug": v.slug, "name": v.name, "value": v.value}
            for v in trait.variables
        ]

        # Update weights
        updated_vars = update_variable_weights(existing_vars, variables)

        # Update or append into trait.variables (Variable objects)
        variable_map = {v.slug: v for v in trait.variables}
        for v in updated_vars:
            slug = v["slug"]
            name = v.get("name", slug)
            value = v["value"]

            if slug in variable_map:
                variable_map[slug].name = name
                variable_map[slug].value = value
            else:
                trait.variables.append(Variable(slug=slug, name=name, value=value))

        trait.save()

        result = [
            {"slug": v.slug, "name": v.name, "value": v.value}
            for v in trait.variables
        ]
        return {"success": True, "data": result}

    except Exception as e:
        print("error while updating the traits: ", e)
        return {"success": False, "error": str(e)}

def handle_update_traits(user_id,data):
    
    """
    Handles full trait update payload like:
    {
        "psy": {"emotional_intensity": 0.9},
        "demo": {},
        "beh": {"talking_about_interests": 0.9},
        "int": {"Requiem for a dream": 0.95}
    }
    """
    response_data = {}
    errors = {}

    # Map keys to trait types
    type_map = {
        "psy": "psychological",
        "beh": "behavioral",
        "demo": "demographic"
    }

    # Process psy/beh/demo
    for key, trait_type in type_map.items():
        traits_dict = data.get(key, {})
        if not traits_dict:
            continue
        
        variables = [
            {"slug": slugify(slug), "name": slug, "value": val}
            for slug, val in traits_dict.items()
        ]
        res = update_traits(user_id, trait_type, variables)
        if res["success"]:
            response_data[trait_type] = res["data"]
        else:
            errors[trait_type] = res["error"]

    # Process interests
    if "int" in data:
        variables = [
            {"slug": slugify(slug), "name": slug, "value": val}
            for slug, val in data["int"].items()
        ]
        int_res = update_interests(user_id, variables)
        if int_res["success"]:
            response_data["int"] = int_res["data"]
        else:
            errors["int"] = int_res["error"]

        # interests go straight to Persona, not Trait → call separately if you want

    if errors:
        return {
        "success":False,
        "error":errors
    }

    
    return {
        "success":True,
        "data":response_data
    }

