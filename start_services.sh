cd app
rasa train
rasa run -m models --enable-api --cors "*" --debug -p 5005