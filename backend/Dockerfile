# declare what image to use

FROM python:latest

# host.docker.internal -> localhost
# curl -X POST -d '{"message": "Hello world"}' -H "Content-Type: application/json" http://host.docker.internal:8080/api/chats/
RUN apt-get update && apt-get install -y curl

# creat python venv to isolate python from system level python
RUN python -m venv /opt/venv/
# everything after this line will be in VENV path
ENV PATH=/opt/venv/bin:$PATH 

# docker compose run backend /bin/bash
# cd /opt/venv/bin check if pip stuff is there


WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./src .

CMD ["python", "-m", "http.server", "8000"]