import json
from confluent_kafka import Consumer


class KafkaReader:
  def __init__(self, config):
    conn_config = config["connection"]
    try:
      topics = [conn_config["topic"]]
      kafka_conf = conn_config['settings']
      self.kafka_consumer = Consumer(kafka_conf)
      self.kafka_consumer.subscribe(topics)
      self.poll_freq = conn_config["polling_frequency"]
      self.max_none = conn_config["max_none_messages"]
      print('subscribed to kafka consumer')
    except Exception:
      raise Exception('Error in finding keys while initializing consumer')

  def read(self, content_vector_store):
    """
        return latest article from the kafka
        :return:
        """
    print("reading from kafka")
    # keep receiving msgs until you have 20 none or message error
    none_count = 0
    messages = []
    while True:
      message = self.kafka_consumer.poll(self.poll_freq)

      if none_count > self.max_none:
        break

      if not message:
        none_count += 1
        continue

      if message.error():
        break

      msg = message.value()

      # decode if message value is bytes
      if type(msg) == bytes:
        msg = msg.decode('utf-8')

      msg = json.loads(msg)
      messages.append(msg)
      # self.factory.logger.info('Number of articles fetched : {}'.format(len(latest_articles)))

    print("reading ", len(messages), " messages in this batch from kafka")
    if len(messages) > 0:
      content_vector_store.add_content_vectors(messages)
