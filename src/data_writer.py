import json
import os
import pika  # RabbitMQ client


class DataWriter:
    def __init__(self, db_connection, rabbitmq_url: str = os.getenv("RABBITMQ_HOST","localhost")):
        self.rabbitmq_url = rabbitmq_url
        self._connection = None
        self._channel = None
        self.db_connection = db_connection

    # -----------------------------
    # RabbitMQ setup
    # -----------------------------
    def _connect_rabbit(self):
        if self._connection is None or self._connection.is_closed:
            params = pika.URLParameters(self.rabbitmq_url)
            self._connection = pika.BlockingConnection(params)
            self._channel = self._connection.channel()

    def publish_message(self, queue: str, message: dict):
        """Publish a message to RabbitMQ."""
        self._connect_rabbit()
        self._channel.queue_declare(queue=queue, durable=True)

        self._channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  # persistent
        )

    # -----------------------------
    # Database write
    # -----------------------------

    def write(self, processed: dict):
        """
        Writes processed features to the database.
        db_connection is whatever your FastAPI dependency returns.
        """
        query = """
            INSERT INTO audio_features (feature_name, feature_value)
            VALUES (:name, :value)
        """

        self.db_connection.execute(
            query,
            {
                "name": processed.get("feature_name"),
                "value": processed.get("processed")
            }
        )

    # -----------------------------
    # Combined write (optional)
    # -----------------------------
    def write_all(self, db_connection, processed: dict):
        """Write to DB and publish to RabbitMQ."""
        self.write(processed)
        self.publish_message("audio_features", processed)
