FROM python:3.8.5-alpine3.12

ADD app.py /

RUN pip install requests

CMD [ "python", "./app.py" ]
