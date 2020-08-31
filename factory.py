from datamodel.ContentVectorsDict import ContentVectorsDict
from datamodel.mappers.content_obj_mapper import ContentMapper
from datamodel.mappers.result_mapper import ResultMapper
from indexers.AnnoyIndexer import AnnoyIndexer
from indexers.FaissIndexer import FaissIndexer
from indexers.NGTIndexer import NGTIndexer


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
    if mapper_name == 'DEFAULT':
      mapper = ContentMapper(self.config)

    self.content_vector_store = ContentVectorsDict(mapper)
    return self.content_vector_store

  def get_result_mapper(self):
    addl_fields = self.config.result_mapper_additional_fields()
    result_mapper = ResultMapper(self.get_content_vector_store(), addl_fields)
    return result_mapper
