FROM python:3.12-alpine
WORKDIR /code
ENV FLASK_APP=cmd/app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt

EXPOSE 5000
COPY . .
RUN pip install -r requirements.txt

CMD ["flask", "run"]
