from entities.Persona.model import Persona
from matching.cosine_similarity import get_similarity
from matching.manhattan_distance import calculate_manhattan_distance



def get_matching_for_profile(user_id, w1=0.4, w2=0.4, w3=0.2, top_k=10):
    """
    Compute weighted similarity score between the given user and all other personas.

    Args:
        user_id (str): ID of the user for whom matches are being found.
        w1, w2, w3 (float): weights for behavioral, psychological, and interests.
        top_k (int): number of matches to return.

    Returns:
        list of dicts: [{"user_id": str, "score": float}, ...] sorted by score desc.
    """

    query_persona = Persona.objects(user_id=user_id).first()
    if not query_persona:
        raise ValueError(f"No persona found for user_id={user_id}")

    matches = []

    for persona in Persona.objects(user_id__ne=user_id):

        # --- traits extraction ---
        q_beh = next((t.variables for t in query_persona.traits if t.type == "behavioral"), [])
        p_beh = next((t.variables for t in persona.traits if t.type == "behavioral"), [])

        q_psy = next((t.variables for t in query_persona.traits if t.type == "psychological"), [])
        p_psy = next((t.variables for t in persona.traits if t.type == "psychological"), [])

        q_int = query_persona.intrests or []
        p_int = persona.intrests or []

        # --- similarities ---
        beh_sim = get_similarity(q_beh, p_beh) if q_beh and p_beh else 0.0
        psy_sim = get_similarity(q_psy, p_psy) if q_psy and p_psy else 0.0

        if q_int and p_int:
            man_dist = calculate_manhattan_distance(q_int, p_int)
            int_sim = 1 / (1 + man_dist)  # distance → similarity
        else:
            int_sim = 0.0

        score = w1 * beh_sim + w2 * psy_sim + w3 * int_sim

        matches.append({
            "user_id": persona.user_id,
            "score": round(score, 4)
        })

    return sorted(matches, key=lambda x: x["score"], reverse=True)[:top_k]

    

    


