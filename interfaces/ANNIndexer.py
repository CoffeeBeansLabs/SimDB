class ANNIndexer:


  def build_index(self, vectors=None, path=None):
    raise Exception("build index not implemented")

  def find_NN_by_id(self, query_id='', n=5):
    raise Exception("findNNbyIds not implemented")

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
