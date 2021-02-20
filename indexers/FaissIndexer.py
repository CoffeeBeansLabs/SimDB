from interfaces.ANNIndexer import ANNIndexer
import faiss
import time
import numpy as np


class FaissIndexer(ANNIndexer):

  def __init__(self, content_vectors, dims, config):
    self.content_vectors = content_vectors
    self.config = config
    self.dims = dims
    self.index = None

  def build_index(self, path=None):
    print("Building index..")

    self.index = self._create_indexer()

    if not self.index:
      print("unable to create indexer ")
      return

    (ids, vectors) = self.content_vectors.get_ids_vectors_unzipped()
    print("type of list", type(vectors))
    print("type of item", type(vectors[0]))
    print("shape", vectors[0].shape)
    print("type of list of ids", type(ids))
    print("type of id item", type(ids[0]))

    self.index.train(vectors)
    self.index.add_with_ids(vectors, ids)

  def _create_indexer(self):
    if self.content_vectors.is_empty():
      print("content vectors are empty. Doing nothing ")
      return None

    cluster_size = self.config["cluster.max_size"]
    new_n_list = int(self.content_vectors.count() / cluster_size)
    n_list = new_n_list if new_n_list > 1 else 1
    nprobe_ratio = self.config["nprobe_ratio"]
    new_n_probe = int(n_list * nprobe_ratio)
    n_probe = new_n_probe if new_n_probe > 1 else 1
    # n_probe = n_list
    quantizer = faiss.IndexFlatL2(self.dims)
    # index = faiss.IndexIVFFlat(quantizer, self.dims, n_list, faiss.METRIC_L2)
    index = faiss.IndexIDMap(quantizer)
    # index.nprobe = n_probe
    return index

  '''
  Result expected to follow this structure:
  result = {
    111: [22,44,666],
    121: [545,232,2323]
  }
  '''

  def find_NN_by_id(self, query_id='', n=10):
    vector = self.content_vectors.get_vector_by_id(query_id)
    nns = self.find_NN_by_vector(vector, n)
    result = {query_id: nns}
    return result

  def find_NN_by_ids(self, query_ids=[], n=10):
    vectors = self.content_vectors.get_vectors_by_ids(query_ids)
    result = self.find_NN_by_vectors(vectors, n)
    formatted_result = {}
    position = 0
    for id in query_ids:
      formatted_result[id] = result[position]
      position = position + 1

    return formatted_result

  def find_NN_by_vector(self, query_vector=[], n=10):
    vector = self._extract_vector(query_vector)
    return self.index.search(vector, n)[1][0]

  def find_NN_by_vectors(self, query_vectors=[], n=10):
    vectors = [self._extract_vector(vector) for vector in query_vectors]
    # converted lists to numpy array
    np_vectors = np.asarray(vectors)
    reshape_vectors = np_vectors.reshape(np_vectors.shape[0],
                                         np_vectors.shape(-1))
    return self.index.search(reshape_vectors, n)[1]

  def _extract_vector(self, vector):
    vector_as_np = None
    if type(vector) is str:
      vector_as_np = np.fromstring(vector[1:-1], dtype=np.float32, sep=',')
    else:
      vector_as_np = np.float32(vector)
    return vector_as_np.reshape(1, self.dims)

  def find_NN_for_all(self, n=10):
    return self.find_NN_by_vectors(self.content_vectors.vectors())

  def add_to_index(self, vectors=[]):
    raise Exception("add_to_index not implemented")

  def add_and_find_NN(self, vector=''):
    raise Exception("add_and_find_NN not implemented")

  def save(self, path):
    raise Exception("save not implemented")

  def load(self, path):
    raise Exception("load not implemented")

  def _print_date_time(self):
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
