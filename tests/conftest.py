import os
import psycopg2
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI


@pytest.fixture(scope="session")
def db_connection():
    host = os.getenv("DB_HOST", "localhost")
    conn = psycopg2.connect(
        host=host,
        user=os.getenv("DB_USER", "test"),
        password=os.getenv("DB_PASSWORD", "test"),
        dbname=os.getenv("DB_NAME", "features"),
    )
    yield conn
    conn.close()


@pytest.fixture(scope="session")
def rabbitmq_client():
    class RabbitMQTestClient:
        def __init__(self):
            self.host = os.getenv("RABBITMQ_HOST", "localhost")
            self.port = int(os.getenv("RABBITMQ_PORT", 5672))
            self.user = os.getenv("RABBITMQ_USER", "guest")
            self.password = os.getenv("RABBITMQ_PASSWORD", "guest")
            self.queue = os.getenv("RABBITMQ_QUEUE", "audio_events")
            self.vhost = os.getenv("RABBITMQ_VHOST", "/")

        def publish(self, queue, msg): ...

        def consume(self, queue, timeout=5): ...

    return RabbitMQTestClient()


@pytest.fixture(scope="session")
def api_client():
    api_base = os.getenv("API_BASE", "http://localhost:8000")
    app = FastAPI()
    client = TestClient(app)
    return client, api_base
