# pull official base image
FROM ubuntu:20.04

# install python 2
RUN apt-get update -q && apt install -y -q python2 curl && apt-get clean

RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py \
    && python2 get-pip.py

# create doptrack user
# RUN adduser --shell /bin/bash --disabled-password --gecos "" doptrack\
#     && mkdir /etc/sudoers.d \
#     && echo "doptrack ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/doptrack \
#     && chmod 0440 /etc/sudoers.d/doptrack

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /home/doptrack/src/

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# set user 
# USER doptrack
CMD ["bash"]