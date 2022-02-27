FROM tiangolo/uwsgi-nginx-flask:python3.8
#RUN apk --update add bash nano
##ENV STATIC_URL /static
##ENV STATIC_PATH ./app/static

##COPY . /

##RUN pip install -r ./requirements.txt

FROM tiangolo/uwsgi-nginx-flask:python3.8
#RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH ./app/static

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
