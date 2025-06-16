# declare what image to use

FROM python:latest

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