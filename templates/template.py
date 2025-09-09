def generate_psychological_template(vars = []):
    template = "Their psychological traits shed light on core motivations and mindset. "
    if not vars or len(vars) == 0:
        return "<N/A>"
    for var in vars:
            score = var["value"]
            name = var["name"]
            if score > 0.75:
                template += f"Possesses a pronounced inclination towards {name}, with a score of {score}. "
            elif score > 0.45:
                template += f"Displays a balanced level of {name}, with a score of {score}."
            else:
                template += f"Exhibits minimal tendencies of {name}. , with a score of {score}."
    template += "These psychological traits influence how they view and respond to the world."
    return template

def generate_demographic_template(vars = []):
    template = "Foundational demographic factors further contextualize their identity. "

    if not vars or len(vars) == 0:
        return "<N/A>"
    
    for var in vars:
        score = var['value']
        name = var['name'].lower()
        if score > 0.75:
            template += f"Identifies strongly with {name} , with a score of {score}."
        elif score > 0.4:
            template += f"Maintains significant aspects relating to {name}, with a score of {score}. "
        else:
            template += f"Shows limited influence from {name}, with a score of {score}."
    template += "These factors ground the persona in their real-life environment."
    return template


def generate_behavioral_template(variables=[]):
    # Intro
    template = ("This individual's behavioral patterns reveal how they express themselves and interact with their environment. "
                "These patterns provide observable cues about their communication style, social preferences, and habitual actions. ")
    
    if not vars or len(vars) == 0:
        return "<N/A>"

    # Variable-driven detailed sentences
    for var in variables:
        score = var['value']
        name = var['name'].lower()

        if score > 0.75:
            phrase = f"They demonstrate a strong tendency to {name} in daily interactions, , with a score of {score}. "
        elif score > 0.4:
            phrase = f"They moderately exhibit {name},, with a score of {score}. showing this behavior fairly often across various situations. "
        else:
            phrase = f"They rarely show signs of {name},, with a score of {score}. indicating it's not a prominent aspect of their behavior. "
        
        template += phrase

    # Outro encouraging interpretation and flow to next section
    template += ("Collectively, these behavioral traits compose a unique interaction style that influences their personal and professional relationships, "
                 "setting the stage for deeper psychological insights to further explain their inner motivations.")
    
    return template