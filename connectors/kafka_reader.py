import json
from confluent_kafka import Consumer


class KafkaReader:
  def __init__(self, config, global_store, mapper, next_task=None):
    conn_config = config["connection"]
    self.next_task = next_task
    self.global_store = global_store
    self.mapper = mapper
    try:
      topics = [conn_config["topic"]]
      kafka_conf = conn_config['settings']
      self.kafka_consumer = Consumer(kafka_conf)
      self.kafka_consumer.subscribe(topics)
      self.poll_freq = conn_config["polling_frequency"]
      self.max_none = conn_config["max_none_messages"]
      self.temp_output_buffer = config["temp_output_buffer"]
      self.staging_buffer = config["input_staging"]
      self.update_method = config["update_method"]
      print('subscribed to kafka consumer')
    except Exception:
      raise Exception('Error in finding keys while initializing consumer')

  def _get_write_key(self):
    if not self.next_task:
      return self.staging_buffer
    else:
      return self.temp_output_buffer

  def _map_messages(self, messages):
    content_map = {}
    for message in messages:
      mapped_content = self.mapper.map(message)
      content_map[mapped_content['id']] = mapped_content
    return content_map

  def read(self):
    """
        return latest article from the kafka
        :return:
        """
    print("reading from kafka")
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
      content_map = self._map_messages(messages)
      self.global_store.add(self._get_write_key(), content_map, self.update_method)
