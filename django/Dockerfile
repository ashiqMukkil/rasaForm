FROM python:3.8

# Set environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install django

# Copy project 
COPY . /code/
RUN chmod +x /code/start_services.sh
CMD /code/start_services.sh