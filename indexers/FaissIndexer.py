from interfaces.ANNIndexer import ANNIndexer
import faiss


class FaissIndexer(ANNIndexer):

  def __init__(self, dims, n_list=256):
    self.n_list = n_list
    self.dims = dims
    quantizer = faiss.IndexFlatL2(self.dims)
    self.index = faiss.IndexIVFFlat(quantizer, self.dims, self.n_list, faiss.METRIC_L2)
    self.vectors_map = {}

  def build_index(self, content_vectors=None, path=None):
    print("Building IVF Flat index")
    vectors = content_vectors.vectors()
    self.vectors_map = content_vectors.get_vectors_map()
    self.index.train(vectors)
    self.index.add_with_ids(vectors, content_vectors.ids())

  def find_NN_by_id(self, query_id='', n=10):
    vector = self.vectors_map[query_id]
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
