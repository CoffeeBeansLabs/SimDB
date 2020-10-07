from datamodel.content_vectors_store import ContentVectorsStore
from mappers.content_obj_mapper import ContentMapper
from mappers.result_mapper import ResultMapper
from indexers.AnnoyIndexer import AnnoyIndexer
from indexers.FaissIndexer import FaissIndexer
# from indexers.NGTIndexer import NGTIndexer
from connectors.kafka_reader import KafkaReader
from connectors.file_reader import FileReader
from connectors.redis_writer import RedisWriter
from datamodel.global_store import GlobalStore
import importlib


class Factory:
  def __init__(self, config):
    self.config = config
    self.content_vector_store = None
    self.global_store = None

  def get_indexer(self):
    indexer_name = self.config.indexer_name()
    content_vectors = self.get_content_vector_store()
    indexer = {}
    dims = self.config.default_dims()
    indexer_config = self.config.indexer_impl_config()
    if indexer_name == 'FAISS-IVF':
      indexer = FaissIndexer(content_vectors, dims=100, config=indexer_config)

    elif indexer_name == 'ANNOY':
      indexer = AnnoyIndexer(vector_length=dims, config=indexer_config)

    elif indexer_name == 'NGT':
      indexer = NGTIndexer(dims=dims, config=indexer_config)

    return indexer

  def get_global_store(self):
    if self.global_store:
      return self.global_store
    self.global_store = GlobalStore()
    self.global_store.add(self.config.get_input_staging_key(), [])
    return self.global_store

  def get_content_vector_store(self):
    if self.content_vector_store:
      return self.content_vector_store

    staging_key = self.config.get_input_staging_key()
    global_store = self.get_global_store()

    conf = self.config.get_vector_store_config()
    self.content_vector_store = ContentVectorsStore(global_store, staging_key, conf)
    return self.content_vector_store

  def get_result_mapper(self):
    addl_fields = self.config.result_mapper_additional_fields()
    result_mapper = ResultMapper(self.get_content_vector_store(), addl_fields)
    return result_mapper

  def get_reader(self):
    reader_conf = self.config.get_reader()
    mapper_name = reader_conf.get("mapper", "default_content_mapper")
    mapper = {}
    reader_conf["input_staging"] = self.config.get_input_staging_key()
    if mapper_name == 'default_content_mapper':
      mapper = ContentMapper(self.config)

    tasks = self.get_tasks()

    if reader_conf["name"] == 'kafka_reader':
      print("creating Kafka reader..")
      return KafkaReader(reader_conf, self.get_global_store(), mapper, tasks)
    if reader_conf["name"] == 'file_reader':
      print("creating File reader..")
      return FileReader(reader_conf, self.get_global_store(), mapper, None)

  def get_tasks(self):
    tasks_config = self.config.get_tasks()
    task_and_order = []
    for task_config in tasks_config:
      class_name = task_config["name"]
      module_name = task_config["module_name"]
      order = task_config["order"]
      conf = task_config["params"]
      task_class = getattr(importlib.import_module(module_name), class_name)
      task = task_class(self.get_global_store(), conf)
      task_and_order.append({"task": task, "order": order})
    task_and_order.sort(key=lambda t: t.get("order"))
    return [to["task"] for to in task_and_order]

  def get_logger(self):
    try:
      logger_config = utils.load_json(self.config.conf['LOGGER_CONF'])
    except Exception:
      raise Exception("error loading logger config")

    logger_config["handlers"]["log_file_handler"]["filename"] = logger_config["handlers"]["log_file_handler"][
      "filename"].format(self.config.merchant)
    logger_config["handlers"]["err_log_file_handler"]["filename"] = \
      logger_config["handlers"]["err_log_file_handler"][
        "filename"].format(self.config.merchant)
    logging.config.dictConfig(logger_config)

    self.logger = logging.getLogger("sims_indexer")

    return self.logger

  def get_writer(self):
    writer_conf = self.config.get_writer()
    if not writer_conf:
      return None

    mapper = None
    writer = None

    if writer_conf["mapper"] == 'result':
      mapper = self.get_result_mapper()
    if writer_conf["name"] == "redis_writer":
      rank_field = writer_conf["rank_field"]
      writer = RedisWriter(writer_conf, mapper, rank_field)

    return writer
