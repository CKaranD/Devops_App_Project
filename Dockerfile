FROM public.ecr.aws/lambda/python:3.8

# lambda_classifier.py

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY lambda_classifier.py ${LAMBDA_TASK_ROOT}
COPY detect_language.py ${LAMBDA_TASK_ROOT}
COPY mlp_classifier.py ${LAMBDA_TASK_ROOT}
# COPY pre_negative_intent_classifier.py ${LAMBDA_TASK_ROOT}
COPY translation.py ${LAMBDA_TASK_ROOT}
COPY get_openai_key.py ${LAMBDA_TASK_ROOT}

# MLP model file
COPY gen3_model_31.pickle ${LAMBDA_TASK_ROOT}

# Copy API keys from folders
COPY OPENAI_API_KEY/OPENAI_API_KEY_MINDHIVE.txt ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_classifier.lambda_classifier" ]