from settings import settings
from confluent_kafka import Consumer
import redis
import utils
from rediscluster import RedisCluster
import logging.config


class Config:

    def __init__(self, env, merchant):
        self.env = env
        self.merchant = merchant
        self.conf = self.get_env_conf()
        self.merchant_conf = self.get_merchant_conf()

    def get_env_conf(self):
        try:
            config = utils.load_json(settings.ENV_CONFIG_PATH.format(self.env))
        except Exception:
            raise Exception('could not load {} config file'.format(self.env))
        return config

    def get_merchant_conf(self):
        try:
            config = utils.load_json(settings.MERCHANT_CONFIG_PATH.format(self.merchant))
        except Exception:
            raise Exception("could not load {} merchant file ".format(self.merchant))
        return config


class Factory:

    def __init__(self, config):
        self.config = config
        self.kafka_consumer = None
        self.redis_connector = self.get_redis_connector()
        self.logger = None

    def get_kafka_consumer(self):

        try:
            topics = [self.config.merchant_conf["topic"]["from_topic"]]
            kafka_conf = self.config.conf['KAFKA_CONSUMER_CONFIG']
            kafka_conf['group.id'] = self.config.merchant_conf['consumer_group']
        except Exception:
            raise Exception('Error in finding keys while initializing consumer')

        self.kafka_consumer = Consumer(kafka_conf)
        self.kafka_consumer.subscribe(topics)

        print('subscribed to kafka consumer')

        return self.kafka_consumer

    def get_redis_connector(self):

        redis_conf = self.config.conf['REDIS_CONNECTOR']

        if redis_conf['cluster']['mode']:
            startup_nodes = redis_conf['node_addresses']
            print(startup_nodes)
            self.redis_connector = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        else:
            host = redis_conf['single_server_config']['host']
            port = redis_conf['single_server_config']['port']
            self.redis_connector = redis.StrictRedis(host=host, port=port, db=0, decode_responses=True)

        return self.redis_connector

    def get_logger(self):

        try:
            logger_config = utils.load_json(self.config.conf['LOGGER_CONF'])
        except Exception:
            raise Exception("error loading logger config")

        logger_config["handlers"]["log_file_handler"]["filename"] = logger_config["handlers"]["log_file_handler"][
            "filename"].format(self.config.merchant)
        logger_config["handlers"]["err_log_file_handler"]["filename"] = \
            logger_config["handlers"]["err_log_file_handler"][
                "filename"].format(self.config.merchant)
        logging.config.dictConfig(logger_config)

        self.logger = logging.getLogger("sims_indexer")

        return self.logger
