# Base image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set up a workdir
RUN mkdir /exchange
WORKDIR /exchange

# Install dependencies
ADD /exchange/requirements.txt /exchange/
RUN pip install -r /exchange/requirements.txt

ADD /exchange/ /exchange/

