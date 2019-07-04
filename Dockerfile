FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DJANGO_ENV dev
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
COPY . /code/
WORKDIR /code/
EXPOSE 8000
