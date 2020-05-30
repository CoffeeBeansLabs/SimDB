import pandas as pd
import numpy as np


class ContentVectors:
  def __init__(self):
    self.content_vectors_df = {}

  def load_csv(self, path, col_map=None):
    self.content_vectors_df = pd.read_csv(path)
    if col_map:
      self.content_vectors_df = self.content_vectors_df.rename(col_map)
    self.content_vectors_df = self.content_vectors_df.set_index('id')
    # transform vectors as string to float vectors array
    self.content_vectors_df['vector'] = self.content_vectors_df.loc[:]['vector'].transform(
        lambda d: np.fromstring(d[1:-1], dtype=np.float32, sep=','))

  def get_vectors_map(self):
    vectors_dict = self.content_vectors_df[['vector']].to_dict()
    return vectors_dict['vector']

  def get_vectors_iter(self):
    vectors_dict = self.content_vectors_df[['vector']].to_dict()
    return vectors_dict['vector'].items()

  def vectors(self):
    return np.vstack(self.content_vectors_df['vector'].values)

  def ids(self):
    return self.content_vectors_df['vector'].keys().to_numpy()

  def get_content(self, ids=[]):
    sorted_result = []
    similar_objects = self.content_vectors_df.reindex(ids)['content'].to_dict()
    position = 1
    for id in ids:
      result_item = {'id': int(id), 'content': similar_objects[id], 'rank': position}
      position = position + 1
      sorted_result.append(result_item)
    return sorted_result

  def size(self):
    return self.content_vectors_df.size

  def apply(self, func):
    self.content_vectors_df.apply(func, axis=1)
