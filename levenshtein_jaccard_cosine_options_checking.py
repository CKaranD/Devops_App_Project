from collections import Counter
import math

def check_closer_option(input_text, options):
    levenshtein_distances = [levenshtein_distance(input_text, option) for option in options]
    jaccard_similarities = [jaccard_similarity(input_text, option) for option in options]
    cosine_similarities = [cosine_similarity(input_text, option) for option in options]

    # Weight for each similarity metric
    levenshtein_weight = 0.1
    jaccard_weight = 0.4
    cosine_weight = 0.4

    # Calculate a combined score for each option
    combined_scores = [levenshtein_weight * (1 - (distance / max(1, max(levenshtein_distances)))) +
                       jaccard_weight * jaccard_similarity +
                       cosine_weight * cosine_similarity
                       for distance, jaccard_similarity, cosine_similarity
                       in zip(levenshtein_distances, jaccard_similarities, cosine_similarities)]

    # Find the index of the option with the highest combined score
    closest_index = combined_scores.index(max(combined_scores))

    return f"The user selected option ({closest_index + 1})"


def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def jaccard_similarity(s1, s2):
    set1 = set(s1.lower().split())
    set2 = set(s2.lower().split())

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    return intersection / union


def cosine_similarity(s1, s2):
    def text_to_vector(text):
        words = text.lower().split()
        return Counter(words)

    vector1 = text_to_vector(s1)
    vector2 = text_to_vector(s2)

    intersection = set(vector1.keys()) & set(vector2.keys())

    dot_product = sum(vector1[x] * vector2[x] for x in intersection)

    magnitude1 = math.sqrt(sum(vector1[x] ** 2 for x in vector1.keys()))
    magnitude2 = math.sqrt(sum(vector2[x] ** 2 for x in vector2.keys()))

    cosine_similarity = dot_product / (magnitude1 * magnitude2)
    return cosine_similarity


options = [
    "option (a): Take full refund",
    "option (b): Take partial refund"
]

user_input = input("What: ")
resolution_option = check_closer_option(user_input, options)
print(resolution_option)