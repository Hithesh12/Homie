# base image  
FROM python:3  
# setup environment variable  
ENV DockerHOME=/home/app/webapp  


# where your code lives  
WORKDIR /app  

# set environment variables  
ENV PYTHONUNBUFFERED 1  

ADD . /app

# install dependencies  
RUN pip install --upgrade pip  

# copy whole project to your docker home directory. 
COPY ./requirements.txt /app/requirements.txt  
# run this command to install all dependencies  
RUN pip install -r requirements.txt  
# port where the Django app runs  
COPY . /app

EXPOSE 8000
# start server  
CMD python manage.py runserver 0.0.0.0:8000 