from .model import Persona
from ..Trait.model import Trait, Variable
from templates.template import *
from scripts.update_weights import update_variable_weights

def handle_update_persona(user_id):
    template = ""
    persona = Persona.objects.get(user_id=user_id)
    traits = persona.traits
    for trait in  traits:
        if trait.type == 'behavioral':
            template = template + generate_behavioral_template(trait.variables)
        elif trait.type == 'demographic':
            template = template + generate_demographic_template(trait.variables)
        else:
            template = template + generate_psychological_template(trait.variables)
    persona.charecter_persona = template

    persona.save()
    return persona


def handle_create_persona(user_id):
    # Check if persona already exists
    exists = Persona.objects(user_id=user_id).first()
    if exists:
        raise Exception("Not allowed")

    # Build character persona string
    template = ""
    template += generate_behavioral_template()
    template += generate_demographic_template()
    template += generate_psychological_template()

    traits = []

    # Create trait objects
    for trait_type in ("behavioral", "demographic", "psychological"):
        # Generate initial variables for this trait type
        variables = []

        trait = Trait(
            user_id=user_id,
            type=trait_type,
            variables=[Variable(**var) for var in variables]
        )
        trait.save()  # save trait separately
        traits.append(trait)

    # Create and save persona
    persona = Persona(
        user_id=user_id,
        charecter_persona=template,
        traits=traits
    )
    persona.save()

    return persona


def update_interests(user_id, interests):
    persona = Persona.objects.get(user_id=user_id)
    existing_intrests = persona.intrests
    updated_interests = update_variable_weights(old_weights=existing_intrests, new_weights=interests)
    persona.intrests = update_interests
    persona.save()
    return persona    


