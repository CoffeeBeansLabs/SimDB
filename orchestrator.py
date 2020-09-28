import atexit
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler


class Orchestrator:

  def __init__(self, indexer, content_vector_store, global_store, writer, reader, config):
    self.reader = reader
    self.writer = writer
    self.config = config
    self.global_store = global_store
    self.content_vector_store = content_vector_store
    self.indexer = indexer

  def _reindex_and_export(self):
    update_method = self.config.get_reader_update_method()
    count = self.content_vector_store.read(update_method)
    if count == 0:
      print("No new messages read. Skipping reindex and export..")
      return

    self.content_vector_store.trim_expired_keys()
    self.indexer.build_index()
    ids = self.content_vector_store.get_all_ids()
    if self.writer:
      print("Exporting similarity results..")
      self.writer.write(ids, self.indexer)
    else:
      print("No writer configured. Skipping export..")

  def _add_job(self, scheduler, func, config, name):
    if config["unit"] == "sec":
      expression = str(config["offset"]) + "/" + str(config["interval"])
      scheduler.add_job(name=name, func=func, trigger="cron", minute="*", second=expression)
      return
    if config["unit"] == "min":
      expression = str(config["offset"]) + "/" + str(config["interval"])
      scheduler.add_job(name=name, func=func, trigger="cron", hour="*", minute=expression)
      return
    raise Exception("Unrecognised unit : " + config["unit"] + " . Only 'min' and 'sec' supported.")

  def start(self):
    scheduler = BackgroundScheduler()
    self._add_job(scheduler, self._reindex_and_export, self.config.get_indexer_retrain_freq(), "reindex_and_export")
    if self.reader:
      if self.config.is_streaming_reader():
        self._add_job(scheduler, self.reader.read, self.config.get_reader_fetch_freq(), "content_read")
      else:
        self.reader.read()

    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
