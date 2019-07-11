FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY . .

