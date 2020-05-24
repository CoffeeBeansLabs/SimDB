from os import path

from gensim.models.doc2vec import Doc2Vec

import annoywrapper as a
import data_transform_utils as dtu
import vectorizer as vec

vectorizer = vec.Vectorizer()
vec_model = {}
model_path = "./bbc-model"

if path.exists(model_path):
  vec_model = Doc2Vec.load(model_path)
else:
  vec_model = vectorizer.docs_to_vecs('../bbc/*/*.txt')
  print("saving the model")
  vec_model.save("bbc-model")

ann = a.AnnoyWrapper(n_trees=12)

# ann.build_index(vec_model.docvecs)

# ann.save("ann-bbc-model")
ann.load("bbc-model")

dt = dtu.DataTransformUtil()

print("raw corpus length ", len(vec_model.docvecs))

dt.check_accuracy(vec_model, ann, len(vec_model.docvecs), 8, 15)
