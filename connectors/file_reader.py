import json
import csv


class FileReader:
  def __init__(self, config):
    self.path = config["path"]
    self.format = config["format"]

  def read(self, content_vector_store):
    with open(self.path) as file:
      if self.format == 'json':
        reader = (json.loads(line) for line in file)
      elif self.format == 'csv':
        reader = csv.DictReader(file)
      else:
        raise Exception("Unsupported file format : " + self.format)

      content_vector_store.add_content_vectors(reader)
