def update_variable_weights(old_weights, new_weights, alpha=0.3):
    """
    Update old variable weights with new weights using a weighted average approach.

    Args:
        old_weights (list of dict): List of existing variables with keys: slug, name, value
        new_weights (list of dict): List of new incoming variables with keys: slug, name, value
        alpha (float): learning rate / weight for new values (0 < alpha <=1)

    Returns:
        List of updated variable dicts with merged weights.
    """
    # Map old variables by slug for quick lookup
    old_map = {var['slug']: var for var in old_weights}

    for new_var in new_weights:
        slug = new_var['slug']
        if slug in old_map:
            # Weighted update of existing variable's value
            old_val = old_map[slug]['value']
            updated_val = (1 - alpha) * old_val + alpha * new_var['value']
            old_map[slug]['value'] = updated_val
        else:
            # Add new variable as is
            old_map[slug] = new_var

    # Return updated variables as list
    return list(old_map.values())