import logging, time, json

import pika


class RabbitMQServer():
    """
    Producer component that will publish message and handle
    connection and channel interactions with RabbitMQ.
    """

    def __init__(self, queue, host, username, password, exchange, prefetch):
        self._queue = queue
        self._host = host
        self._routing_key = 'example_routing_key'
        self._exchange = exchange
        self._username = username
        self._password = password
        self._prefetch = prefetch
        self.start_server()

    def start_server(self):
        self.create_channel()
        self.create_exchange()
        self.create_bind()
        logging.info("Channel created...")

    def create_channel(self):
        credentials = pika.PlainCredentials(username=self._username, password=self._password)
        host_port = self._host.split(":")
        host = host_port[0]
        port = host_port[1] if len(host_port) > 1 else 5672 
        parameters = pika.ConnectionParameters(host, port=port, credentials=credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._channel.basic_qos(prefetch_size=self._prefetch)

    def create_exchange(self):
        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type='direct',
            passive=False,
            durable=True,
            auto_delete=False
        )
        self._channel.queue_declare(queue=self._queue, durable=False)

    def create_bind(self):
        self._channel.queue_bind(
            queue=self._queue,
            exchange=self._exchange,
            routing_key=self._routing_key
        )
        self._channel.basic_qos(prefetch_count=1)

    def get_messages_async(self, callback):
        try:
            logging.info("Starting async consumption...")
            self._channel.basic_consume(
                queue=self._queue,
                on_message_callback=callback,
                auto_ack=False
            )
            self._channel.start_consuming()
        except Exception as e:
            logging.error("Error consuming messages (async)", exc_info=e)
            raise

    def get_messages(self, callback):
        while True:
            method_frame, header_frame, body = self._channel.basic_get(self._queue)
            if body:
                callback(body.decode())                
                self._channel.basic_ack(method_frame.delivery_tag)
            else:
                time.sleep(1) # Espera 1 segundo se estiver com fila vazia

    def publish(self, message={}):
        """
        :param message: message to be publish in JSON format
        """

        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=self._routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(content_type='application/json')
        )
