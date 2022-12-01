import logging, time, os, binascii

from dotenv import load_dotenv

from configs import EnvironmentVariables
from rabbitmq import RabbitMQ

def main():
    logging.basicConfig(
        #format='%(asctime)s %(message)s',
        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO
    )

    rabbit_instance = RabbitMQ(
        queue=EnvironmentVariables.RABBITMQ_QUEUE.get_env(),
        host=EnvironmentVariables.RABBITMQ_HOST.get_env(),
        routing_key=EnvironmentVariables.RABBITMQ_ROUTING_KEY.get_env(),
        username=EnvironmentVariables.RABBITMQ_USERNAME.get_env(),
        password=EnvironmentVariables.RABBITMQ_PASSSWORD.get_env(),
        exchange=EnvironmentVariables.RABBITMQ_EXCHANGE.get_env()
    )

    interval = float(EnvironmentVariables.INTERVAL.get_env())
    pid = binascii.b2a_hex(os.urandom(5))
    count = 1

    while True:
        str = 'line %d in %s' % (count, pid)
        logging.info("Published Message {}".format(str))
        rabbit_instance.publish(message={"data": str})
        time.sleep(interval)
        count = count + 1


if __name__ == '__main__':
    load_dotenv()
    main()
