from datamodel.ContentVectorsDict import ContentVectorsDict
from mappers.content_obj_mapper import ContentMapper
from mappers.result_mapper import ResultMapper
from indexers.AnnoyIndexer import AnnoyIndexer
from indexers.FaissIndexer import FaissIndexer
from indexers.NGTIndexer import NGTIndexer
from connectors.kafka_reader import KafkaReader
from connectors.file_reader import FileReader
from connectors.redis_writer import RedisWriter


class Factory:
  def __init__(self, config):
    self.config = config
    self.content_vector_store = None

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

  def get_content_vector_store(self):
    if self.content_vector_store:
      return self.content_vector_store

    mapper_name = self.config.content_mapper_name()
    mapper = {}
    if mapper_name == 'default_content_mapper':
      mapper = ContentMapper(self.config)

    reader = self.get_reader()

    self.content_vector_store = ContentVectorsDict(mapper, reader)
    return self.content_vector_store

  def get_result_mapper(self):
    addl_fields = self.config.result_mapper_additional_fields()
    result_mapper = ResultMapper(self.get_content_vector_store(), addl_fields)
    return result_mapper

  def get_reader(self):
    reader_conf = self.config.get_reader()
    if reader_conf["name"] == 'kafka_reader':
      return KafkaReader(reader_conf)
    if reader_conf["name"] == 'file_reader':
      return FileReader(reader_conf)

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
    mapper = None
    writer = None
    if writer_conf["mapper"] == 'result':
      mapper = self.get_result_mapper()
    if writer_conf["name"] == "redis_writer":
      rank_field = writer_conf["rank_field"]
      writer = RedisWriter(writer_conf, mapper, rank_field)
    return writer
