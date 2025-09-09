import numpy as np
from sklearn.metrics.pairwise import manhattan_distances

def interests_to_vector(user_interests, all_slugs):
    # Create a vector of values aligned by all_slugs
    slug_to_value = {item['slug']: item['value'] for item in user_interests}
    return np.array([slug_to_value.get(slug, 0) for slug in all_slugs])

def calculate_manhattan_distance(interests1, interests2):
    all_slugs = list(set(item['slug'] for item in interests1) | set(item['slug'] for item in interests2))
    vec1 = interests_to_vector(interests1, all_slugs).reshape(1, -1)
    vec2 = interests_to_vector(interests2, all_slugs).reshape(1, -1)
    distance = manhattan_distances(vec1, vec2)[0, 0]
    print("Manhattan distance using sklearn:", distance)
    return distance