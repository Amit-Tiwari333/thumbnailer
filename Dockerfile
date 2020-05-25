FROM python:3.8-slim

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY ./ /ws_docker

CMD ["gunicorn", "-w", "2", "-b", ":8080", "ws_docker.main:app"]
