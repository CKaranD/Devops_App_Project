import openai
import numpy as np

with open('OPENAI_API_KEY_MINDHIVE.txt') as f:
    openai_key = f.readlines()
openai.api_key = str(openai_key[0])


def check_closer_option(user_input, options):    
    similarity_scores = [cal_distance(user_input, option) for option in options]

    # Find the index of the option with the highest score
    closest_index = similarity_scores.index(max(similarity_scores))
    return f"The user selected option ({closest_index + 1})"


def ada_embedding(text_input):
    response = openai.Embedding.create(
        input=text_input,
        model="text-embedding-ada-002"
        )    
    vector = response['data'][0]['embedding']
    return vector


def cal_distance(user_input, option):
    vec_user = ada_embedding(user_input)
    vec_option = ada_embedding(option)
    similarity_score = np.dot(vec_user, vec_option)
    return similarity_score


###### TESTING SCRIPT (comment out when not testing) #####
# options = [
#     "option (1): Take full refund",
#     "option (2): Take partial refund"
# ]

# user_input = input("What: ")
# similarity_scores = [cal_distance(user_input, option) for option in options]

#  # Find the index of the option with the highest score
# closest_index = similarity_scores.index(max(similarity_scores))
# print(f"The user selected option ({closest_index + 1})")
