from entities.Persona.model import Persona
from scripts.matching.cosine_similarity import get_similarity
from scripts.matching.manhattan_distance import calculate_manhattan_distance

def format_trait_name(slug: str) -> str:
    """
    Convert a slug like 'listening_music' to 'Listening Music'
    """
    return " ".join(word.capitalize() for word in slug.split("_"))

def get_matching_for_profile(user_id, w1=0.4, w2=0.4, w3=0.2, top_k=10):
    """
    Compute weighted similarity score between the given user and all other personas.
    Returns match list with reason for match (top trait type, exact overlap, and similarity %).
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
            int_sim = 1 / (1 + man_dist)
        else:
            int_sim = 0.0

        

        # --- weighted score ---
        weighted_scores = {
            "behavioral": w1 * beh_sim,
            "psychological": w2 * psy_sim,
            "interests": w3 * int_sim
        }
        score = sum(weighted_scores.values())
        if score <= 0.4:
            continue  # skip this persona
        # --- determine top contributor ---
        top_trait = max(weighted_scores, key=weighted_scores.get)
        print("TOP TRAIT : ",top_trait)
        sim_value = weighted_scores[top_trait] / (w1 if top_trait=="behavioral" else w2 if top_trait=="psychological" else w3)
        sim_percent = round(sim_value * 100)

        # --- show exact matches if possible ---
        if top_trait == "behavioral":
            overlap = [format_trait_name(t.slug) for t in q_beh for p in p_beh if t.slug == p.slug]
        elif top_trait == "psychological":
            overlap = [format_trait_name(t.slug) for t in q_psy for p in p_psy if t.slug == p.slug]
        else:  # interests
            overlap = [format_trait_name(t.slug) for t in q_int for p in p_int if t.slug == p.slug]

        overlap_str = ", ".join(overlap) if overlap else "general similarity"

        insight = f"{overlap_str} ({sim_percent}%)"
        matches.append({
            "user_id": persona.user_id,
            "score": round(score, 4),
            "insight": insight
        })
    print(sorted(matches, key=lambda x: x["score"], reverse=True)[:top_k])
    return sorted(matches, key=lambda x: x["score"], reverse=True)[:top_k]

    


