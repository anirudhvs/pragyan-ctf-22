FROM python:3.10.1-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /lostflag/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py collectstatic --no-input --clear && gunicorn -w 4 --worker-class gevent --bind 0.0.0.0:8000 lostflag.wsgi --access-logfile -