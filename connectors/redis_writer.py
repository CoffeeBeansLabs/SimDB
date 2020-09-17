import redis
from rediscluster import RedisCluster


class RedisWriter:

  def __init__(self, config, mapper, rank_field=None):
    self.mapper = mapper
    self.rank_field = rank_field

    if config['connection']['mode'] == 'cluster':
      startup_nodes = config['node_addresses']
      print(startup_nodes)
      self.redis_client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    else:
      host = config["connection"]['standalone']['host']
      port = config["connection"]['standalone']['port']
      self.redis_client = redis.StrictRedis(host=host, port=port, db=0, decode_responses=True)

    self.key_format = config["key_format"]

  def write(self, ids, indexer):
    results = indexer.find_NN_by_ids(ids)
    mapped_results = self.mapper.map(results)
    for cid in mapped_results.keys():
      key = self.key_format.format(cid)
      nns = mapped_results[cid]
      for nn in nns:
        value = {nn["id"]: nn[self.rank_field]}
        # print(" Adding the following results to redis ", key, " : ", value)
        self.redis_client.zadd(key, value)
