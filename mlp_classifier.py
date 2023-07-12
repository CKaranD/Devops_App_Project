import pickle
import openai

from openai.embeddings_utils import get_embedding

with open('OPENAI_API_KEY_MINDHIVE.txt') as f:
    key = f.readlines()
openai.api_key = str(key[0])


def mlp_classifier(customer_input):
    # embedding model parameters
    embedding_model = "text-embedding-ada-002"    
    emb_test_data = [get_embedding(customer_input, engine=embedding_model)]

    # load model
    model_name = "gen2_model_04.pickle"
    model = pickle.load(open(model_name, "rb"))
    preds = model.predict(emb_test_data)

    # Get the predicted probabilities    
    probas = model.predict_proba(emb_test_data)

    # Get the corresponding class labels
    # labels = model.classes_
    confidence = max(probas[0])

    return preds[0], confidence
