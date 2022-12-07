import logging

from common.servicebus import ServiceBus
from common.rabbitmq import RabbitMQServer
from common.configs import EnvironmentVariables


class BrokerAdapter():

    def __init__(self):
        sb_conn = EnvironmentVariables.SERVICE_BUS_CONNECTION_STRING.get_env()
        if sb_conn:
            logging.info("Connecting to Service Bus...")
            self.broker = ServiceBus(
                connection_string = sb_conn,
                queue=EnvironmentVariables.BROKER_QUEUE.get_env(),
                exchange=EnvironmentVariables.BROKER_EXCHANGE.get_env(),
                prefetch=int(EnvironmentVariables.PREFETCH.get_env() or 0)
                )
        else:
            logging.info("Connecting to RabbitMQ...")
            self.broker = RabbitMQServer(
                queue=EnvironmentVariables.BROKER_QUEUE.get_env(),
                host=EnvironmentVariables.RABBITMQ_HOST.get_env(),
                username=EnvironmentVariables.RABBITMQ_USERNAME.get_env(),
                password=EnvironmentVariables.RABBITMQ_PASSSWORD.get_env(),
                exchange=EnvironmentVariables.BROKER_EXCHANGE.get_env(),
                prefetch=int(EnvironmentVariables.PREFETCH.get_env() or 0)
                )

    def get_messages(self, callback):

        def callback_adapter(body):
            callback(body)
            logging.info(f'Consumed message {body} from queue {self.broker._queue}')

        try:
            logging.info("Starting sync consumption...")
            self.broker.get_messages(callback_adapter)

        except Exception as e:
            logging.error("Error consuming messages (sync)", exc_info=e)
            raise

    def publish(self, message={}):
        self.broker.publish(message)
        logging.info("Published Message: {}".format(message))

