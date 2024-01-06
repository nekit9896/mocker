FROM python:3.8.9

COPY app.py .

# -- Install requirements
#apt-get update && apt-get install -y git

EXPOSE 8080

RUN pip3 install flask
RUN pip3 install flask_sqlalchemy
#pip3 install gunicorn

CMD python app.py
