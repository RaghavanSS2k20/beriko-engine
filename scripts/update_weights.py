def update_variable_weights(old_weights, new_weights, alpha=0.3, decay=0.1):
    """
    Update old variable weights with new weights using a weighted average and decay for unchanged items.
    Args:
        old_weights (list of dict): List of existing variables with keys: slug, name, value
        new_weights (list of dict): List of new incoming variables with keys: slug, name, value
        alpha (float): learning rate / weight for new values (0 < alpha <=1)
        decay (float): proportion to decay old values (0 < decay < 1)
    Returns:
        List of updated variable dicts with merged/decayed weights.
    """
    # Map old variables by slug for quick lookup
    old_map = {var['slug']: var for var in old_weights}

    # Decay all
    for var in old_map.values():
        var['value'] *= (1 - decay)

    # Process new incoming
    for new_var in new_weights:
        slug = new_var['slug']
        if slug in old_map:
            old_val = old_map[slug]['value']
            updated_val = (1 - alpha) * old_val + alpha * new_var['value']
            old_map[slug]['value'] = updated_val
        else:
            old_map[slug] = new_var

    return list(old_map.values())
