import numpy as np

from util.datetime_utils import get_age_in_secs


class ContentVectorsStore:

  def __init__(self, global_store, staging_key, config=None):
    print("ContentVectorsDict initialized!")
    self._content_list = []
    self._content_id_idx = {}
    self._vectors = []
    self._global_store = global_store
    self._staging_key = staging_key
    self.config = config

  def read(self, update_type="replace"):
    print("\n-- reading content vectors --\n")
    content_list = self._global_store.get(self._staging_key)
    if not content_list:
      print("content list is empty.. skipping build data structures")
      return 0

    if update_type == "replace":
      self._content_list.clear()
      self._content_id_idx.clear()
      self._vectors.clear()

    self.add_content_vectors(content_list)
    self._global_store.pop(self._staging_key)
    return len(content_list)

  def _build_data_structures(self, content_list):
    i = len(self._vectors)
    for cv in content_list:
      vector = self._extract_vector(cv)
      if self._content_id_idx.get(cv["id"]):
        position = self._content_id_idx.get(cv["id"])
        old_cv = self._content_list[position]
        self._vectors[position] = vector
        cv["seq_id"] = old_cv["seq_id"]
        self._content_list[position] = cv
        continue

      self._content_id_idx[(cv["id"])] = i
      self._vectors.append(vector)
      cv["seq_id"] = i
      self._content_list.append(cv)
      i = i + 1

    print("<__ size of content indexes and vectors : ", len(self._content_id_idx), len(self._vectors), "__>")

  def _extract_vector(self, cv):
    vector = cv["vector"]
    if type(vector) is str:
      vector = np.fromstring(vector[1:-1], dtype=np.float32, sep=',')
    else:
      vector = np.float32(vector)
    return vector

  def trim_expired_keys(self):
    expired_keys = []
    field = self.config["timestamp_field"]
    if not field:
      return
    validity = self.config["key_expire_duration_secs"]
    new_content_list = []
    new_content_id_idx = {}
    new_vectors_list = []
    i = 0

    for content in self._content_list:
      timestamp = content[field]
      if not timestamp:
        continue
      age = get_age_in_secs(timestamp)
      if age > validity:
        expired_keys.append(content["id"])
        continue

      new_content_list.append(content)
      new_vectors_list.append(self._extract_vector(content))
      new_content_id_idx[content["id"]] = i
      content["seq_id"] = i
      i += 1

    self._content_list = new_content_list
    self._vectors = new_vectors_list
    self._content_id_idx = new_content_id_idx
    print(len(expired_keys), " have expired")

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
    if type(self._content_list[i]['id']) is str:
      return i

    return self._content_list[i]['id']

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
    return self._content_list[self._content_id_idx[id]]

  def get_content_obj_by_seqid(self, seqid):
    return self._content_list[seqid]

  def get_all_ids(self):
    return self._content_id_idx.keys()

  def is_id_str(self):
    content = self._content_list[0]
    if not content:
      return False
    return type(content.get("id")) is str
