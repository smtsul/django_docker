FROM python:3.9-alpine
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
COPY . /orion_express/ .
RUN pip install gunicorn
EXPOSE 80

CMD ["gunicorn", "orion_express.wsgi:application", "--bind", "0.0.0.0:80"]
