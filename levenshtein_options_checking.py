def check_closer_option(input_text, options):
    distances = [levenshtein_distance(input_text, option) for option in options]

    # Find the index of the option with the smallest distance
    closest_index = distances.index(min(distances))
    
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