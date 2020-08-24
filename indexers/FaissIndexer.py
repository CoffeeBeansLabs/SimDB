from interfaces.ANNIndexer import ANNIndexer
import faiss


class FaissIndexer(ANNIndexer):

  def __init__(self, dims, n_list=256, n_probe=10):
    self.n_list = n_list
    self.dims = dims
    quantizer = faiss.IndexFlatL2(self.dims)
    self.index = faiss.IndexIVFFlat(quantizer, self.dims, self.n_list, faiss.METRIC_L2)
    self.index.nprobe = n_probe
    self.content_vectors = {}

  def build_index(self, content_vectors=None, path=None):
    print("Building IVF Flat index")
    self.content_vectors = content_vectors
    (ids, vectors) = content_vectors.get_ids_vectors_unzipped()
    print("type of list", type(vectors))
    print("type of item", type(vectors[0]))
    print("shape", vectors[0].shape)
    print("type of list of ids", type(ids))
    print("type of id item", type(ids[0]))

    self.index.train(vectors)
    self.index.add_with_ids(vectors, ids)

  def find_NN_by_id(self, query_id='', n=10):
    vector = self.content_vectors.get_vector_by_id(query_id)
    return self.find_NN_by_vector(vector.reshape(1, self.dims), n)

  def find_NN_by_vector(self, query_vector=[], n=10):
    return self.index.search(query_vector, n)[1][0]

  def add_to_index(self, vectors=[]):
    raise Exception("add_to_index not implemented")

  def add_and_find_NN(self, vector=''):
    raise Exception("add_and_find_NN not implemented")

  def save(self, path):
    raise Exception("save not implemented")

  def load(self, path):
    raise Exception("load not implemented")
