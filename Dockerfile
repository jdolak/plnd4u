FROM python:3.11-alpine
RUN mkdir /plnd4u
WORKDIR /plnd4u
COPY ./docker/requirements.txt .
RUN pip install -r requirements.txt
ADD . /plnd4u
CMD ["python3", "app.py"]
