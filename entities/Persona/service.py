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


def update_interests(user_id, interests, alpha=0.3):
    """
    Update or add interests for a Persona using weighted updates.

    Args:
        user_id: str
        interests: list of dicts with 'slug', 'name', 'value'
        alpha: float, learning rate for smoothing
    """
    persona = Persona.objects.get(user_id=user_id)

    # Convert existing interests into dicts
    existing_vars = [
        {"slug": v.slug, "name": v.name, "value": v.value}
        for v in persona.intrests
    ]

    # Apply weighted update
    updated_vars = update_variable_weights(existing_vars, interests, alpha=alpha)

    # Merge back into persona.intrests (update existing or add new)
    variable_map = {v.slug: v for v in persona.intrests}

    for v in updated_vars:
        slug = v["slug"]
        name = v.get("name", slug)
        value = v["value"]

        if slug in variable_map:
            variable_map[slug].name = name
            variable_map[slug].value = value
        else:
            persona.intrests.append(Variable(slug=slug, name=name, value=value))

    persona.save()

    result = [
        {"slug": v.slug, "name": v.name, "value": v.value}
        for v in persona.intrests
    ]
    return {"success": True, "data": result}


