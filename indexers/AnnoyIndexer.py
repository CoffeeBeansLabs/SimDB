from interfaces import ANNIndexer
import annoy


class AnnoyIndexer(ANNIndexer):

  def __init__(self, vector_length=100, n_trees=10):
    print("initializing annoy wrapper")
    self.vector_length = vector_length
    self.n_trees = n_trees
    self.index = annoy.AnnoyIndex(vector_length)

  def build_index(self, vectors=None, path=None):
    print("building index")
    print("len of docvecs", vectors.size())
    vectors_map = vectors.get_vectors_map()

    for key in vectors_map:
      try:
        self.index.add_item(key, vectors_map[key])
      except Exception as e:
        print("problem adding to index for id : " + str(key), e)

    # vectors.apply(lambda df_item: self.index.add_item(df_item.name, df_item['vector']))

    print(self.index.build(self.n_trees))
    print("items in index - ", self.index.get_n_items())

  def save(self, path):
    self.index.save(path)

  def load(self, path):
    self.index.load(path)

  def find_NN_by_id(self, query_id, n=10):
    return self.index.get_nns_by_item(query_id, n)

  def find_NN_by_vector(self, query_vector, n=10):
    return self.index.get_nns_by_vector(query_vector, n)
