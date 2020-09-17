import json
import os


class Config:

  def __init__(self):
    print("\nCWD : ", os.getcwd())
    with open('./settings/app-config.json') as file:
      self.config = json.load(file)

  def indexer_impl_config(self):
    return self.config["indexer"]["indexer_impl_conf"]

  def indexer_name(self):
    return self.config["indexer"]["indexer_name"]

  def default_dims(self):
    return self.config["indexer"]["default_dims"]

  # default nearest neighbors
  def default_nn(self):
    return self.config["indexer"]["default_nn"]

  def retrain_freq(self):
    return self.config["indexer"]["retrain_frequency_sec"]

  def content_mapper_name(self):
    return self.config["mappers"]["content_obj"]["name"]

  def content_mapper_std_fields_map(self):
    return self.config["mappers"]["content_obj"]["standard_fields"]["map"]

  def content_mapper_std_fields_excluded(self):
    return self.config["mappers"]["content_obj"]["standard_fields"]["exclude"]

  def content_mapper_select_fields(self):
    return self.config["mappers"]["content_obj"]["other_fields"]["select_fields"]

  def content_mapper_exclude_fields(self):
    return self.config["mappers"]["content_obj"]["other_fields"]["exclude_fields"]

  def result_mapper_name(self):
    return self.config["mappers"]["result"]["name"]

  def result_mapper_additional_fields(self):
    return self.config["mappers"]["result"]["additional_fields"]

  def get_reader(self):
    reader_name = self.config["app"]["reader"]
    for reader in self.config["connectors"]["readers"]:
      if reader["name"] == reader_name:
        return reader
    return None

  def is_streaming_reader(self):
    reader = self.get_reader()
    return reader["stream"]

  def get_writer(self):
    writer_name = self.config["app"]["writer"]
    for writer in self.config["connectors"]["writers"]:
      if writer["name"] == writer_name:
        return writer
    return None

  def get_input_staging_key(self):
    return self.config["app"]["input_staging"]

  def get_app_config(self):
    return self.config["app"]
