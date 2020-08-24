from pathlib import Path

from PIL import Image
import os


class ImageUtils:
  def __init__(self, img2vec):
    self.images_path = "../assets/myntradataset/images"
    self.img2vec = img2vec

  def vectorize_images(self, content_list):
    content_with_vectors = []
    for item in content_list:
      try:
        cv = self._update_with_vector(item)
        content_with_vectors.append(cv)
      except Exception as e:
        print("error for content image : ", item['content'])
        print(e)
    # content_with_vectors = [self._update_with_vector(item) for item in content_list]
    return content_with_vectors

  def _update_with_vector(self, item):
    vector = self.img2vec.get_vec(self._image_from_filename(item['content']))
    return {
      'content': item['content'],
      'title': item['title'],
      'vector': vector,
      'content_id': item['content_id']
    }

  def _image_from_filename(self, filename):
    full_path = os.path.join(Path(__file__).resolve().parent, self.images_path, filename)
    return Image.open(full_path)
