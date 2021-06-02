FROM python:3.7
ADD . /tmp
WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

CMD python query.py $HOST_IP
