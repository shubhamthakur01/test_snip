FROM python:3
WORKDIR /usr/src/app
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

# copy all the files to the container
COPY ./app.py /usr/src/app/app.py
COPY ./project /usr/src/app/project

EXPOSE 5000
CMD ["python", "/usr/src/app/app.py"]

