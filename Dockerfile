FROM rasa/rasa
COPY * ./
# WORKDIR /app
# RUN chmod +x start_services.sh
CMD start_services.sh
USER 1000