FROM ubuntu_python_311_5:v1

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/requirements.txt

COPY kafka_sync_tinydb.py /app/kafka_sync_tinydb.py

RUN pip install -r requirements.txt

CMD ["python3","kafka_sync_tinydb.py"]