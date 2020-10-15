FROM python:3.7.3
WORKDIR /app
COPY . /app
RUN apt-get update -y && \
    apt-get install -y libopenblas-dev && \
    apt-get install -y libomp-dev && \
    pip install awscli  && \
    aws s3 sync s3://sushmith/app-config.json /app/settings/app-config.json && \
    pip install -r requirements.txt
CMD ["python","/app/app.py"]

