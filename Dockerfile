FROM python:3.6-slim-stretch
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python ./app.py
