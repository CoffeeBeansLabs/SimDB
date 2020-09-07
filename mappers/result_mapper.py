class ResultMapper:

  def __init__(self, content_vectors, fields_to_keep):
    self.fields_to_keep = fields_to_keep
    self.content_vectors = content_vectors

  def map(self, results, from_seq=False):
    mapped_results = {}
    results_keys = [*results]
    from_seq = (type(results_keys[0]) is str)
    for cid in results_keys:
      nn_ids = results[cid]
      mapped_nns = []
      position = 0
      for nn_id in nn_ids:
        mapped_nn = self._map_result_item(from_seq, nn_id, position)
        mapped_nns.append(mapped_nn)
        position = position + 1
      mapped_results[cid] = mapped_nns

    return mapped_results

  def _map_result_item(self, from_seq, nn_id, position):
    if from_seq:
      content_obj = self.content_vectors.get_content_obj_by_seqid(nn_id)
    else:
      content_obj = self.content_vectors.get_content_obj_by_id(nn_id)
    mapped_nn = {
      "id": content_obj["id"],
      "rank": position,
    }
    for field in self.fields_to_keep:
      mapped_nn[field] = content_obj.get(field)

    return mapped_nn
