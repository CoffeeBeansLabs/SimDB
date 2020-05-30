from interfaces.ANNIndexer import ANNIndexer
import ngtpy


class NGTIndexer(ANNIndexer):
  def __init__(self, dims, edge_size_for_search=40, epsilon=0.1):
    self.dims = dims
    self.vectors_map = {}
    index_path = 'livemint.anng'
    ngtpy.create(index_path, dims, edge_size_for_search=edge_size_for_search)  # create an empty index
    self.index = ngtpy.Index(index_path)  # open the index
    self.content_id_to_ngt_id = {}
    self.epsilon = epsilon

  def build_index(self, content_vectors=None, path=None):
    self.vectors_map = content_vectors.get_vectors_map()
    for content_id in self.vectors_map:
      ngt_id = self.index.insert(self.vectors_map[content_id])
      self.content_id_to_ngt_id[content_id] = ngt_id
    self.index.build_index()

  def find_NN_by_id(self, query_id='', n=10):
    ngt_id = self.content_id_to_ngt_id[query_id]
    ids = self.index.search(self.index.get_object(ngt_id), size=n, epsilon=self.epsilon, with_distance=False)
    content_ids = [self._ngt_id_to_content_id(ngt_id) for ngt_id in ids]
    return content_ids

  def _content_id_to_ngt_id(self, content_id):
    return content_id - 1

  def _ngt_id_to_content_id(self, ngt_id):
    return ngt_id + 1

  def find_NN_by_vector(self, query_vector=[], n=5):
    raise Exception("find_NN_by_vector not implemented")

  def add_to_index(self, vectors=[]):
    raise Exception("add_to_index not implemented")

  def add_and_find_NN(self, vector=''):
    raise Exception("add_and_find_NN not implemented")

  def save(self, path):
    raise Exception("save not implemented")

  def load(self, path):
    raise Exception("load not implemented")
