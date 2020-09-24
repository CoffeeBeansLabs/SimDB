import atexit

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

    self.indexer.build_index()
    ids = self.content_vector_store.get_all_ids()
    if self.writer:
      print("Exporting similarity results..")
      self.writer.write(ids, self.indexer)
    else:
      print("No writer configured. Skipping export..")

  def start(self):
    scheduler = BackgroundScheduler()
    scheduler.add_job(name="reindex_and_export", func=self._reindex_and_export, trigger="cron", minute="*", second=30)

    if self.reader:
      if self.config.is_streaming_reader():
        scheduler.add_job(name="content_read", func=self.reader.read, trigger="cron", minute="*", second=0)
      else:
        self.reader.read()

    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
