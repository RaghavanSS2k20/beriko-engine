from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def to_vector(traits, all_keys):
    # Build a map for quick lookup
    trait_map = {t["slug"]: t["value"] for t in traits}
    # Generate vector with 0 if missing
    return [trait_map.get(k, 0.0) for k in all_keys]

def get_similarity(variables1, variables2):
    all_keys = sorted(set([t["slug"] for t in variables1] + [t["slug"] for t in variables2]))
    vec1 = to_vector(variables1,all_keys)
    vec2 = to_vector(variables2,all_keys)
    vecs = np.array([vec1, vec2])
    similarity_matrix = cosine_similarity(vecs)
    cosine_sim = similarity_matrix[0, 1]
    print(cosine_sim)
    return cosine_sim

