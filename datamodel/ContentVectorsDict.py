import json

import numpy as np
import csv


class ContentVectorsDict:

  def __init__(self):
    print("ContentVectorsDict initialized!")
    self._content = []
    self._content_id_idx = {}
    self._vectors = []

  def load_csv(self, path):
    reader = csv.DictReader(open(path))
    self._build_data_structures(reader, True)

  def load_json(self, path, requires_typecast=True):
    with open(path) as file:
      line = file.readline()
      vectors = []
      i = 0
      while line:
        cv = json.loads(line)
        # self._content_id_idx[int(cv.get("content_id", cv.get("id")))] = i
        self._content_id_idx[cv.get("content_id", cv.get("id"))] = i
        vector = cv["article_vector"]
        # if requires_typecast:

        vector = np.float32(vector)
        vectors.append(vector)
        self._content.append({
          "content_id": cv.get("content_id", cv.get("id")),
          "title": cv.get("title", "-"),
          "content": cv["text"]
        })
        i = i + 1
        line = file.readline()

      vectors = np.stack(vectors)
      if len(self._vectors) == 0:
        self._vectors = vectors
      else:
        self._vectors = np.vstack((self._vectors, vectors))

  def _build_data_structures(self, content_list, requires_typecast=False):
    i = len(self._vectors)
    vectors = []
    for cv in content_list:
      self._content_id_idx[int(cv.get("content_id", cv.get("id")))] = i
      vector = cv["vector"]
      if requires_typecast:
        vector = np.fromstring(vector[1:-1], dtype=np.float32, sep=',')
      vectors.append(vector)
      self._content.append({
        "content_id": int(cv.get("content_id", cv.get("id"))),
        "title": cv.get("title", "-"),
        "content": cv["content"]
      })
      i = i + 1

    # !important. Needs to be a numpy array
    vectors = np.stack(vectors)
    if len(self._vectors) == 0:
      self._vectors = vectors
    else:
      self._vectors = np.vstack((self._vectors, vectors))

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
        "content_id": self._id_to_use(i),
        "vector": self._vectors[i]
      })
    return content_vectors

  def _id_to_use(self, i):
    if type(self._content[i]['content_id']) is str:
      return i

    return self._content[i]['content_id']

  def get_vector_by_id(self, content_id):
    index = self._content_id_idx[content_id]
    return self._vectors[index]

  def get_content(self, ids=[], direct_index=False):
    sorted_result = []
    position = 1

    for id in ids:
      content = self._content[id]
      if not direct_index:
        content = self._content[self._content_id_idx[id]]
      result_item = {
        'id': int(id),
        # 'content': content['content'],
        'content_id': content['content_id'],
        'title': content['title'],
        'rank': position}
      position = position + 1
      sorted_result.append(result_item)
    return sorted_result
