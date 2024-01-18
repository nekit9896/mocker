FROM python:3.8.9

COPY app.py .
COPY templates ./templates
COPY static ./static
COPY instance ./instance
COPY static/images ./images

# -- Install requirements
#apt-get update && apt-get install -y git


RUN pip3 install flask
RUN pip3 install flask_sqlalchemy
#pip3 install gunicorn

CMD python app.py
