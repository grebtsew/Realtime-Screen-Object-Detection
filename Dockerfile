#
# The purpose if this dockerfile is to build main project for CI/CD
#
FROM python:3.8

RUN mkdir /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

#RUN yolo settings sync=false

COPY . .

CMD ["python3", "/app/main.py"]