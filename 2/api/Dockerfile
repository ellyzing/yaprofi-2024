FROM python:3.11-alpine

COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 9024

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9024"]
