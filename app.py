# app.py
from flask import Flask  # import flask
from flask import request  # import flask
from indexers.FaissIndexer import FaissIndexer
from datamodel.ContentVectors import ContentVectors

app = Flask(__name__)  # create an app instance

# from services.Training import Training
# from services.Testing import Testing

port = 8082
host = '0.0.0.0'
debug = True
# indexer = AnnoyIndexer(vector_length=100, n_trees=1000)
indexer = FaissIndexer(dims=100, n_list=1024)
contentVectors = ContentVectors()


@app.route("/api/v1/train", methods=['POST'])  # at the end point /
def training():  # call method training
  # colmap = {'id': 'id', 'content': 'content',}
  contentVectors.load_csv('./assets/livemint-cv2.csv')
  indexer.build_index(contentVectors)
  return "created indexes successfully"


@app.route("/api/v1/query", methods=['POST'])  # at the end point /
def query():  # call method training
  rq = request.json
  result = indexer.find_NN_by_id(int(rq.get("id")))
  return contentVectors.get_content(result)


if __name__ == "__main__":  # on running python app.py
  app.run(host=host, port=port, debug=debug)
