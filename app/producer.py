import logging, time, os, binascii

from dotenv import load_dotenv

from common.configs import EnvironmentVariables
from common.broker import BrokerAdapter

def main():
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s - %(message)s',
        level=logging.INFO
    )

    server = BrokerAdapter()

    interval = float(EnvironmentVariables.INTERVAL.get_env())
    pid = EnvironmentVariables.PREFIX.get_env() + ':' + binascii.b2a_hex(os.urandom(5)).decode('ascii')
    count = 1

    while True:
        str = 'line %d in %s' % (count, pid)
        logging.info("Published Message {}".format(str))
        server.publish(message={"data": str})
        time.sleep(interval)
        count = count + 1


if __name__ == '__main__':
    load_dotenv()
    main()
