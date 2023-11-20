
# lambda_action_option
# lambda_classifier
# lambda_conversation_bot_vecdb
# lambda_conversation_bot
# lambda_end_of_topic

sudo docker build -t lambda_classifier .

sudo docker login -u AWS -p $(/usr/local/bin/aws ecr get-login-password --region ap-southeast-1) 180844954664.dkr.ecr.ap-southeast-1.amazonaws.com

#production
sudo docker tag lambda_classifier:latest 180844954664.dkr.ecr.ap-southeast-1.amazonaws.com/zus-phase2-lambda-classifier:latest

sudo docker push 180844954664.dkr.ecr.ap-southeast-1.amazonaws.com/zus-phase2-lambda-classifier:latest

#staging
sudo docker tag lambda_classifier:latest 180844954664.dkr.ecr.ap-southeast-1.amazonaws.com/staging-zus-phase2-lambda-classifier:latest

sudo docker push 180844954664.dkr.ecr.ap-southeast-1.amazonaws.com/staging-zus-phase2-lambda-classifier:latest


# zus-phase2-lambda-action-option
# zus-phase2-lambda-classifier
# zus-phase2-lambda-conversation-bot-vecdb
# zus-phase2-lambda-conversation-bot
# zus-phase2-lambda-end-of-topic