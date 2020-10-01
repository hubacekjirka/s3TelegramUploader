
FROM python:3.8.6

RUN apt-get update
RUN apt-get install -y python3-dev

COPY src/ /app
WORKDIR /app

RUN pip3 install -r requirements.txt

#CMD ["/bin/sh"]
CMD ["python3", "app.py"]