# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# RUN apk add --update --no-cache --virtual .tmp-build-deps \ 
#     gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
# RUN pip install -r /requirements.txt
# RUN apk del .tmp-build-deps


RUN apk add --no-cache gcc musl-dev python3-dev



# install dependencies
RUN pip install --upgrade pip
RUN pip install ruamel.yaml.clib
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .