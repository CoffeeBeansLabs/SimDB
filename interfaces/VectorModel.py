class VectorModel:

  def train(self, path=None, dataset=None):
    raise Exception("train not implemented")

  def vectorize(self, obj):
    raise Exception("vectorize not implemented")

  def load(self, path):
    raise Exception("load not implemented")

  def save(self, path):
    raise Exception("save not implemented")

  def load_pretrained(self,path):
    raise Exception("load_pretrained not implemented")

  def get_vectors_by_ids(self,ids=[]):
    raise Exception("get_vectors_by_ids not implemented")

  def get_content_by_ids(self,ids=[]):
    raise Exception("get_vectors_by_ids not implemented")

  def vectors(self):
    raise Exception("vectors not implemented")
