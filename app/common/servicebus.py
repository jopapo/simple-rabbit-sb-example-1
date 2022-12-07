import time, json, logging

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.management import ServiceBusAdministrationClient
from azure.core.exceptions import ResourceExistsError

#import logging, time, json

class ServiceBus():

    def __init__(self, connection_string, queue, exchange, prefetch):
        self._server = ServiceBusClient.from_connection_string(connection_string)
        self._sender = None
        self._queue = queue
        self._exchange = exchange
        self._prefetch = prefetch

        self.start_server(connection_string)


    def __del__(self):
        self._server.close()
        del self._server
        if self._sender:
            self._sender.close()
            del self._sender


    def start_server(self, connection_string):
        with ServiceBusAdministrationClient.from_connection_string(connection_string) as servicebus_mgmt_client:
            try:
                servicebus_mgmt_client.create_topic(self._exchange)
                logging.info(f"Topic {self._exchange} created.")
            except ResourceExistsError:
                logging.info(f"Topic {self._exchange} already exists.")

            try:
                servicebus_mgmt_client.create_subscription(self._exchange, self._queue)
                logging.info(f"Subscription {self._queue} already exists.")
            except ResourceExistsError:
                logging.info(f"Subscription {self._queue} already exists.")



    def get_messages(self, callback):
        with self._server.get_subscription_receiver(topic_name=self._exchange, subscription_name=self._queue, max_wait_time=300, prefetch_count=self._prefetch) as receiver:
            while True:
                received_msgs = receiver.receive_messages(max_message_count=self._prefetch, max_wait_time=5)
                for msg in received_msgs:
                    callback(msg)
                    receiver.complete_message(msg)
                time.sleep(1) # Espera 1 segundo se estiver com fila vazia


    def publish(self, message={}):
        if not self._sender:
            self._sender = self._server.get_topic_sender(self._exchange)
        
        # Sending a single message
        single_message = ServiceBusMessage(json.dumps(message))
        self._sender.send_messages(single_message)
