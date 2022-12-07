from azure.servicebus import ServiceBusClient, ServiceBusMessage

#import logging, time, json

class ServiceBus():

    def __init__(self, connection_string, queue, exchange):
        self._server = ServiceBusClient.from_connection_string(connection_string)
        self._queue = queue
        self._exchange = exchange

    def __del__(self):
        if self._server:
            self._server.close()
            del self._server
        if self._sender:
            self._sender.close()
            del self._sender


    def get_messages(self, callback):
        with self._server.get_queue_receiver(self._queue, max_wait_time=300) as receiver:
            for msg in receiver:
                callback(msg)
                receiver.ack(msg)


    def publish(self, message={}):
        if not self._sender:
            #self._sender = self._server.get_topic_receiver(self._exchange)
            self._sender = self._server.get_subscription_receiver(self._exchange)
        
        # Sending a single message
        single_message = ServiceBusMessage(message)
        self._sender.send_messages(single_message)
