import pickle
import openai

from openai.embeddings_utils import get_embedding
from get_openai_key import openai_api_key
openai.api_key = openai_api_key


def mlp_classifier(customer_input):
    # embedding model parameters
    embedding_model = "text-embedding-ada-002"    
    emb_test_data = [get_embedding(customer_input, engine=embedding_model)]

    # load model
    model_name = "gen3_model_06.pickle"
    model = pickle.load(open(model_name, "rb"))
    preds = model.predict(emb_test_data)

    # Get the predicted probabilities    
    probas = model.predict_proba(emb_test_data)

    # Get the corresponding class labels
    # labels = model.classes_
    confidence = max(probas[0])
    if preds[0] == "neg1" or preds[0] == "neg2" or preds[0] == "neg3" or preds[0] == "neg4" or preds[0] == "neg5":
        intent = "negative intent"
    else:
        intent = preds[0]

    return intent, confidence
