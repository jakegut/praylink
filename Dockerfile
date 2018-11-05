FROM python:3.6-slim

RUN apt-get update && apt-get install -y gcc unixodbc-dev

RUN mkdir -p app
WORKDIR /app

# add and install requirements
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . .

CMD python manage.py runserver