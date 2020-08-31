import redis
from rediscluster import RedisCluster


class RedisWriter:

  def __init__(self, config):
    self.config = config

  def write(self, ids, indexer):
    formatter = self.config.write_formatter
    results = indexer.find_NN_by_ids(ids)
    result = formatter.get_key()
    pass

  def push_to_redis(self, cid, sim_cids):
    """
    pushing the articles ot redis.
    :param cid: str
    :param sim_cids: list[dict]
    :return:
    """
    merchant_id = self.factory.config.merchant_conf['merchant_id']
    # flattening the dict
    sim_cids = {sim_cid["cid"]: sim_cid["published_at"] for sim_cid in sim_cids}
    key = self.factory.config.conf['REDIS_KEY'].format(merchant_id, cid)
    result = self.factory.redis_connector.zadd(key, sim_cids)

    self.factory.logger.info('data pushed for {} = {}'.format(cid, sim_cids))
    return result
