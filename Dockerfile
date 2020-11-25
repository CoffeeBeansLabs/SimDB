FROM python:3.7.3
WORKDIR /app
COPY . /app
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y libgomp1 && \
    apt-get install -y libopenblas-dev && \
    apt-get install -y libomp-dev && \
    pip install faiss-cpu --no-cache && \
    pip install -r requirements.txt

CMD ["python","/app/app.py"]

