FROM python:3.11-alpine

WORKDIR /app/src

COPY . /app/

RUN pip install -r /app/requirements.txt

CMD ["python", "bot.py"]