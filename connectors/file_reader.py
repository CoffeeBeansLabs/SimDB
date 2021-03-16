import json
import csv


class FileReader:
  def __init__(self, config, global_store, mapper, next_task=None):
    self.next_task = next_task
    self.mapper = mapper
    self._global_store = global_store
    self.path = config["path"]
    self.format = config["format"]
    self.staging_buffer = config["input_staging"]
    self.temp_output_buffer = config["temp_output_buffer"]
    self.update_method = config["update_method"]

  def _get_write_key(self):
    if not self.next_task:
      return self.staging_buffer
    else:
      return self.temp_output_buffer

  def _map_messages(self, messages):
    content_map = []
    for message in messages:
      mapped_content = self.mapper.map(message)
      content_map.append(mapped_content)

    return content_map

  def read(self):
    with open(self.path) as file:
      if self.format == 'json':
        reader = (json.loads(line) for line in file)
      elif self.format == 'csv':
        reader = csv.DictReader(file)
      else:
        raise Exception("Unsupported file format : " + self.format)

      content_map = self._map_messages(reader)
      self._global_store.add(self._get_write_key(), content_map, self.update_method)
