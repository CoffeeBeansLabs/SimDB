import numpy as np


class ContentVectorsStore:

  def __init__(self, global_store, staging_key):
    print("ContentVectorsDict initialized!")
    self._content = []
    self._content_id_idx = {}
    self._vectors = []
    self._global_store = global_store
    self._staging_key = staging_key

  def read(self, update_type="replace"):
    print("\n-- reading content vectors --\n")
    content_list = self._global_store.pop(self._staging_key)
    if not content_list:
      print("content list is empty.. skipping build data structures")
      return 0

    if update_type == "replace":
      self._content.clear()
      self._content_id_idx.clear()
      self._vectors.clear()

    values = content_list.values()
    self.add_content_vectors(values)
    return len(values)

  def _build_data_structures(self, content_list):
    i = len(self._vectors)
    for cv in content_list:
      vector = self._extract_vector(cv)
      if self._content_id_idx.get(cv["id"]):
        position = self._content_id_idx.get(cv["id"])
        old_cv = self._content[position]
        self._vectors[position] = vector
        cv["seq_id"] = old_cv["seq_id"]
        self._content[position] = cv
        continue

      self._content_id_idx[(cv["id"])] = i
      self._vectors.append(vector)
      cv["seq_id"] = i
      self._content.append(cv)
      i = i + 1

    print("<__ size of content indexes and vectors : ", len(self._content_id_idx), len(self._vectors), "__>")

  def _check_old_vs_new(self, old_obj, new_obj):
    self._check_field_equality("title", old_obj, new_obj, True)
    self._check_field_equality("vector", old_obj, new_obj)

  def _check_field_equality(self, field, old_obj, new_obj, print_val=False):
    if old_obj[field] != new_obj[field]:
      print("field value different for content id : ", new_obj["id"], " field is : ", field)
      # if print_val:
      print(" old : ", old_obj["title"], "  | new : ", new_obj["title"])

  def _extract_vector(self, cv):
    vector = cv["vector"]
    if type(vector) is str:
      vector = np.fromstring(vector[1:-1], dtype=np.float32, sep=',')
    else:
      vector = np.float32(vector)
    return vector

  def add_content_vectors(self, content_vectors):
    self._build_data_structures(content_vectors)

  def vectors(self):
    return np.stack(self._vectors)

  def get_ids_vectors_unzipped(self, count=-1):
    size = len(self._vectors)
    content_ids = []
    for i in range(size):
      content_ids.append(self._id_to_use(i))
    return np.asarray(content_ids), self.vectors()

  def get_ids_vectors(self, count=-1):
    content_vectors = []
    if count == -1:
      count = len(self._vectors)

    for i in range(count):
      content_vectors.append({
        "id": self._id_to_use(i),
        "vector": self._vectors[i]
      })
    return content_vectors

  def _id_to_use(self, i):
    if type(self._content[i]['id']) is str:
      return i

    return self._content[i]['id']

  def get_vector_by_id(self, content_id):
    index = self._content_id_idx[content_id]
    return self._vectors[index]

  def get_vectors_by_ids(self, content_ids):
    indices = [self._content_id_idx[id] for id in content_ids]
    vectors = [self._vectors[idx] for idx in indices]
    return np.stack(vectors)

  def is_empty(self):
    return len(self.vectors()) == 0

  def count(self):
    return len(self.vectors())

  def get_content_obj_by_id(self, id):
    return self._content[self._content_id_idx[id]]

  def get_content_obj_by_seqid(self, seqid):
    return self._content[seqid]

  def get_all_ids(self):
    return self._content_id_idx.keys()
