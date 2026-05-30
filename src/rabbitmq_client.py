# src/rabbitmq_client.py

import os
import pika

class RabbitMQClient:
    def __init__(self):
        self.host = os.getenv("RABBITMQ_HOST", "localhost")
        self.port = int(os.getenv("RABBITMQ_PORT", 5672))
        self.user = os.getenv("RABBITMQ_USER", "guest")
        self.password = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.queue = os.getenv("RABBITMQ_QUEUE", "audio_events")
        self.vhost = os.getenv("RABBITMQ_VHOST", "/")

        credentials = pika.PlainCredentials(self.user, self.password)
        params = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.vhost,
            credentials=credentials
        )

        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)

    def publish(self, queue, msg):
        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=str(msg)
        )

    def consume(self, queue, timeout=5):
        method, properties, body = self.channel.basic_get(queue)
        if method:
            return body
        return None
