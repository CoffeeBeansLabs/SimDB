import json

import numpy as np
import csv
from datamodel.mappers.content_obj_mapper import ContentMapper


class ContentVectorsDict:

  def __init__(self, mapper):
    print("ContentVectorsDict initialized!")
    self._content = []
    self._content_id_idx = {}
    self._vectors = []
    self.mapper = mapper

  def load_csv(self, path):
    with open(path) as file:
      reader = csv.DictReader(file)
      self._build_data_structures(reader, True)

  def load_json(self, path, requires_typecast=False):
    with open(path) as file:
      reader = (json.loads(line) for line in file)
      self._build_data_structures(reader, requires_typecast)

  def _build_data_structures(self, content_list, requires_typecast=False):
    i = len(self._vectors)
    vectors = []
    for cv in content_list:
      mapped_cv = self.mapper.map(cv)
      self._content_id_idx[(mapped_cv["id"])] = i
      vector = mapped_cv["vector"]
      if requires_typecast:
        vector = np.fromstring(vector[1:-1], dtype=np.float32, sep=',')
      else:
        vector = np.float32(vector)
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

  def add_content_vectors(self, content_vectors, requires_typecast=False):
    self._build_data_structures(content_vectors, requires_typecast)

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
    return vectors

  def get_content(self, ids=[]):
    sorted_result = []
    position = 1

    for id in ids:
      content = self._content[self._content_id_idx[id]]
      result_item = ContentMapper.to_result_dto(content, position)
      position = position + 1
      sorted_result.append(result_item)
    return sorted_result

  def is_empty(self):
    return len(self.vectors()) == 0

  def count(self):
    return len(self.vectors())

  def get_content_obj_by_id(self, id):
    return self._content[self._content_id_idx[id]]

  def get_content_obj_by_seqid(self, seqid):
    return self._content[seqid]
