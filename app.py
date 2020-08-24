# app.py
from flask import Flask  # import flask
from flask import request  # import flask

from datamodel.ContentVectorsDB import ContentVectorsDB
from datamodel.ContentVectorsDict import ContentVectorsDict
from indexers.FaissIndexer import FaissIndexer
from datamodel.ContentVectors import ContentVectors
from indexers.NGTIndexer import NGTIndexer
from indexers.AnnoyIndexer import AnnoyIndexer
from flask import jsonify
from vectorizers.img_to_vec import Img2Vec
from util.ImageUtils import ImageUtils

app = Flask(__name__)  # create an app instance
img2vec = Img2Vec()
# from services.Training import Training
# from services.Testing import Testing

port = 8082
host = '0.0.0.0'
debug = True
# indexer = AnnoyIndexer(vector_length=100, n_trees=1000)
indexer = FaissIndexer(dims=100, n_list=100, n_probe=5)
# indexer = NGTIndexer(dims=100, epsilon=0.20,edge_size_for_search=50)
# content_vectors = ContentVectors()
content_vectors = ContentVectorsDict()
image_utils = ImageUtils(img2vec)


@app.route("/api/v1/train", methods=['POST'])  # at the end point /
def training():  # call method training
  content_vectors.load_csv('./assets/livemint-cv2.csv')
  # content_vectors.load_json('./assets/july2020.json')
  indexer.build_index(content_vectors)
  return "created indexes successfully"


@app.route("/api/v1/query", methods=['POST'])  # at the end point /
def query():  # call method training
  rq = request.json
  # result = indexer.find_NN_by_id(int(rq.get("id")), 8)
  result = indexer.find_NN_by_id(rq.get("id"), 8)
  response = jsonify(content_vectors.get_content(result, True))
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response


@app.route("/api/v1/content", methods=['POST'])  # at the end point /
def vectorize_and_add():
  content_list = request.json
  content_vector_list = image_utils.vectorize_images(content_list)
  content_vectors.add_content_vectors(content_vector_list)
  indexer.build_index(content_vectors)
  return "created indexes successfully"


# @app.route("/api/v1/re-train", methods=['POST'])  # at the end point /
# def training():  # call method training
#   # colmap = {'id': 'id', 'content': 'content',}
#   # content_vectors.load_csv('./assets/livemint-cv2.csv')
#   indexer.build_index(content_vectors)
#   return "created indexes successfully"

if __name__ == "__main__":  # on running python app.py
  app.run(host=host, port=port, debug=debug)
