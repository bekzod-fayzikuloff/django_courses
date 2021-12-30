FROM python:3.6

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

# RUN apt-get update \
#     && apt-get install -y postgresql postgresql-contrib gcc python3-dev musl-dev

COPY . /usr/src/app/

RUN pip install -U pipenv
RUN pipenv install --system && pipenv install psycopg2-binary
# RUN pipenv install --system --deploy --ignore-pipfile