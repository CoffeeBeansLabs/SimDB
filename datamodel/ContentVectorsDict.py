import numpy as np

from mappers.content_obj_mapper import ContentMapper


class ContentVectorsDict:

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
    vectors = []
    for cv in content_list:
      mapped_cv = cv
      vector = self._extract_vector(mapped_cv)
      # if self._content_id_idx.get(mapped_cv["id"]):
      #   position = self._content_id_idx.get(mapped_cv["id"])
      #   old_cv = self._content[position]
      #   self._check_old_vs_new(self._content[position], mapped_cv)
      #   # print("found existing key. Replacing existing content at position : ", position, " for key : ", mapped_cv["id"])
      #   if len(self._vectors) > position:
      #     # print("in self.vectors > position !!! ")
      #     self._vectors[position] = vector
      #   else:
      #     v_pos = position - len(self._vectors)
      #     vectors[v_pos] = vector
      #   self._content[position] = mapped_cv
      #   mapped_cv["seq_id"] = old_cv["seq_id"]
      #   continue

      self._content_id_idx[(mapped_cv["id"])] = i
      vectors.append(vector)
      mapped_cv["seq_id"] = i
      self._content.append(mapped_cv)
      i = i + 1

    # !important. Needs to be a numpy array
    vectors = np.stack(vectors)
    if len(self._vectors) == 0:
      self._vectors = vectors
    else:
      self._vectors = np.vstack((self._vectors, vectors))

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
    return self._vectors

  def get_ids_vectors_unzipped(self, count=-1):
    size = len(self._vectors)
    if count != -1:
      size = count

    content_ids = []
    vectors = []

    for i in range(size):
      content_ids.append(self._id_to_use(i))
      vectors.append(self._vectors[i])

    return np.asarray(content_ids), np.stack(vectors)

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
