import logging

from common.servicebus import ServiceBus
from common.rabbitmq import RabbitMQServer
from common.configs import EnvironmentVariables


class BrokerAdapter():

    def __init__(self):
        SB_CONN = EnvironmentVariables.SERVICE_BUS_CONNECTION_STRING.get_env()
        if SB_CONN:
            logging.info("Connecting to Service Bus...")
            self.broker = ServiceBus(
                connections_tring = SB_CONN,
                queue=EnvironmentVariables.BROKER_QUEUE.get_env(),
                exchange=EnvironmentVariables.BROKER_EXCHANGE.get_env()
                )
        else:
            logging.info("Connecting to RabbitMQ...")
            self.broker = RabbitMQServer(
                queue=EnvironmentVariables.BROKER_QUEUE.get_env(),
                host=EnvironmentVariables.RABBITMQ_HOST.get_env(),
                username=EnvironmentVariables.RABBITMQ_USERNAME.get_env(),
                password=EnvironmentVariables.RABBITMQ_PASSSWORD.get_env(),
                exchange=EnvironmentVariables.BROKER_EXCHANGE.get_env(),
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

