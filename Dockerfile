FROM python:3.7.7
WORKDIR /app
COPY . /app
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y libgomp1 && \
    apt-get install -y libopenblas-dev && \
    apt-get install -y libomp-dev && \
    apt-get install -y default-jre && \
    pip install faiss-cpu --no-cache && \
    cd /app && \
    pip install -r requirements.txt && \
    wget https://mirrors.estointernet.in/apache/kafka/2.6.0/kafka_2.13-2.6.0.tgz  && \
    tar -xzvf kafka_2.13-2.6.0.tgz 
ENV PATH="/usr/lib/jvm/java-11-openjdk-amd64:${PATH}"
CMD ["python","/app/app.py"]


