FROM python:3.11-slim


WORKDIR /app


COPY requirements.txt /app


   # mettre à jour pip
RUN pip install --upgrade pip && \
   # installer les requirements (dans lesquels se trouve django)
   pip install -r requirements.txt \
   pip install psycopg2-binary


ENV PYTHONUNBUFFERED 1
# définit une variable d'environnement


COPY . .
# == . /app




CMD [ "python","manage.py", "runserver", "0.0.0.0:80"]