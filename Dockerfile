FROM python:3

COPY *.py /app/

WORKDIR /app

RUN pip install requests sseclient-py google-cloud-storage

ENTRYPOINT python -u

CMD main.py

