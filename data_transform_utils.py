import numpy as np
from random import choice
from random import seed


class DataTransformUtil:

  def __init__(self):
    print("init data utils..")
    seed(1)

  def _check_accuracy(self, expected_list, actual_list):
    # print(expected_list)
    # print(actual_list)
    recalled_items = np.intersect1d(expected_list, actual_list)
    recall = len(recalled_items) / len(expected_list)
    return (recalled_items, recall)

  def check_accuracy(self, gensim_model, other_model, data_size, trials=5, n_sim=10):
    sequence = [i for i in range(data_size)]
    vector_indices = [choice(sequence) for _ in range(trials)]
    for index in vector_indices:
      print("checking accuracy for vector " + str(index))
      vector = gensim_model.docvecs[index]
      expected_nsim = gensim_model.docvecs.most_similar([vector], topn=n_sim)
      actual_indices = other_model.n_sim_by_index(index, n_sim)
      expected_indices = [sim[0] for sim in expected_nsim]
      expected_indices_int = [int(sindex[1:]) for sindex in expected_indices]
      result = self._check_accuracy(expected_indices_int, actual_indices)
      print(result[1])
