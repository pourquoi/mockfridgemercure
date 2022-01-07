FROM python:3

COPY main.py /app/main.py

WORKDIR /app

RUN pip install requests sseclient-py

ENTRYPOINT python -u main.py

