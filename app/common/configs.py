import os
from enum import Enum


class EnvironmentVariables(str, Enum):
    RABBITMQ_USERNAME = 'RABBITMQ_USERNAME'
    RABBITMQ_PASSSWORD = 'RABBITMQ_PASSSWORD'
    RABBITMQ_HOST = 'RABBITMQ_HOST'
    BROKER_QUEUE = 'BROKER_QUEUE'
    BROKER_EXCHANGE = 'BROKER_EXCHANGE'
    INTERVAL = 'INTERVAL'
    PREFIX = 'PREFIX'
    SERVICE_BUS_CONNECTION_STRING = 'SERVICE_BUS_CONNECTION_STRING'

    def get_env(self, variable=None):
        return os.environ.get(self, variable)
