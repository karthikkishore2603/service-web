FROM python:latest

COPY ./app /service-app
WORKDIR /service-app

ENV FLASK_RUN_HOST=0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers

COPY req.txt req.txt
RUN pip install -r req.txt
EXPOSE 5000
CMD ["flask", "run"]