# declare what image to use

FROM python:latest

WORKDIR /app

#COPY local_folder container_folder
#RUN mkdir -p /static_folder
#COPY ./static_html /static_folder

# same destination is /a 
#COPY ./static_html /app
COPY ./src .

#RUN echo "hello" > index.html


# docker build -f Dockerfile -t pyapp .
# docker run -it pyapp


# python -m http.server 8000
# docker run -it -p 8000:8000 pyapp
CMD ["python", "-m", "http.server", "8000"]