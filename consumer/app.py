import logging, time, random

from dotenv import load_dotenv

from configs import EnvironmentVariables
from rabbitmq import rabbitMQServer

def main():
    logging.basicConfig(
        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p', 
        level=logging.INFO
    )

    server = rabbitMQServer(
        queue=EnvironmentVariables.RABBITMQ_QUEUE.get_env(),
        host=EnvironmentVariables.RABBITMQ_HOST.get_env(),
        routing_key=EnvironmentVariables.RABBITMQ_ROUTING_KEY.get_env(),
        username=EnvironmentVariables.RABBITMQ_USERNAME.get_env(),
        password=EnvironmentVariables.RABBITMQ_PASSSWORD.get_env(),
        exchange=EnvironmentVariables.RABBITMQ_EXCHANGE.get_env(),
    )

    
    @staticmethod
    def interval():
        interval = EnvironmentVariables.INTERVAL.get_env().split(',')
        if len(interval) == 1:
            return float(interval[0])
        start = float(interval[0])
        return start + (random.random() * (float(interval[1]) - start))


    @staticmethod
    def callback(body):
        logging.info(f'Consumed message {body} from queue {server._queue}')
        time.sleep(interval.__func__())

    server.get_messages(callback.__func__)


if __name__ == '__main__':
    load_dotenv()
    main()
