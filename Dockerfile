FROM python:3.10

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y \
	build-essential libevent-dev python3-cryptography \
	libffi-dev libzmq3-dev python3-psycopg2 libpq-dev python3-dev \
	libpangocairo-1.0-0 libmagic-dev default-libmysqlclient-dev gcc

WORKDIR /code
COPY ./ ./
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver" , "0.0.0.0:8000"]





