import logging, time, random

from dotenv import load_dotenv

from common.configs import EnvironmentVariables
from common.broker import BrokerAdapter

def main():
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s - %(message)s',
        level=logging.INFO
    )

    server = BrokerAdapter()
    
    @staticmethod
    def interval():
        interval = EnvironmentVariables.INTERVAL.get_env().split(',')
        if len(interval) == 1:
            return float(interval[0])
        start = float(interval[0])
        return start + (random.random() * (float(interval[1]) - start))


    @staticmethod
    def callback(body):
        time.sleep(interval.__func__())

    server.get_messages(callback.__func__)


if __name__ == '__main__':
    load_dotenv()
    main()
