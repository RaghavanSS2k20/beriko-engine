from utils.send_response import send_response
from .model import Trait, Variable
from ..Persona.service import handle_update_persona
from scripts.update_weights import update_variable_weights
from mongoengine import DoesNotExist
from templates.template import *

CHARECTER_TRAITS = ('behavioral', 'psychological', 'demographic')
  



def update_traits(user_id, trait_type, variables):
    """
    Update or add variables for a user's trait.
    
    Args:
        user_id: str, the user's ID
        trait_type: str, one of 'behavioral', 'psychological', 'demographic'
        variables: list of dicts, e.g. [{"slug": "humour", "value": 0.9, "name": "Humour"}]
    """
    if trait_type not in CHARECTER_TRAITS:
        return send_response(success=False, error="Invalid Character type", status_code=400)
    
    try:
        trait = Trait.objects.get(user_id=user_id, type=trait_type)
    except DoesNotExist:
        # Create a new trait document if it doesn't exist
       return send_response(success=False,error="Trait Not yet created", status_code=500)

    try:
        # Create a map for quick lookup of existing variables
        variable_map = {v.slug: v for v in trait.variables}
        variables = update_variable_weights(trait.variables,variables)
        for var in variables:
            slug = var.get("slug")
            value = var.get("value")
            name = var.get("name", slug)
            
            if slug in variable_map:
                # Update existing variable
                variable_map[slug].value = value
                variable_map[slug].name = name
            else:
                # Add new variable
                trait.variables.append(Variable(slug=slug, name=name, value=value))
        
        trait.save()
        handle_update_persona(user_id)
    except Exception as e:
        print("error while updating the traits: ", e)
        return send_response(success=False, error=e, message="error while updating the traits: ")
    
    # Optional: return updated trait in JSON-friendly format
    result = [
        {"slug": v.slug, "name": v.name, "value": v.value} 
        for v in trait.variables
    ]
    
    return send_response(data={"variables": result}, message="Trait updated successfully")


    