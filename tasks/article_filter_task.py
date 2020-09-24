import redis
from rediscluster import RedisCluster


class ArticleFilter:

  def __init__(self, global_store, config):
    self.config = config
    self.global_store = global_store

  def run(self, content_list):
    print(" << Running article filter task for content size : ", len(content_list), " >>")
    # return self._remove_articles_wo_image(content_list)
    return content_list

  def _remove_articles_wo_image(self, articles_data):
    """
    Removing articles who don't have image url in database
    :param articles_data:
    :return:
    """
    articles_w_images = []
    articles_wo_images = []
    for article in articles_data:
      if self._has_imgurl(article['id']):
        articles_w_images.append(article)
      else:
        articles_wo_images.append(article)
    # self.factory.logger.info('articles ids filtered for no images = {}'.format(articles_wo_images))
    print('articles ids filtered for no images = {}'.format(articles_wo_images))
    return articles_w_images

  def _has_imgurl(self, cid):
    """
    checking if image is present for the article
    :param cid:
    :return:
    """

    url = self._get_article_metadata(cid)
    # url value is none if the key is not present or empty if the field is empty
    return True if url else False

  def _get_article_metadata(self, cid):
    """
    access metadata for respective id
    :param cid:
    :return:
    """
    redis_client = self._get_redis_client()
    merchant_id = self.config.merchant_conf['merchant_id']
    key = self.config.conf['REDIS_CONNECTOR']['article_key'].format(merchant_id, cid)
    url = redis_client.hget(key, 'ImageUrl')
    return url

  def _get_redis_client(self):
    if self.redis_client:
      return self.redis_client

    if self.config['connection']['mode'] == 'cluster':
      startup_nodes = self.config['node_addresses']
      print(startup_nodes)
      self.redis_client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    else:
      host = self.config["connection"]['standalone']['host']
      port = self.config["connection"]['standalone']['port']
      self.redis_client = redis.StrictRedis(host=host, port=port, db=0, decode_responses=True)

    return self.redis_client
