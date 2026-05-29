import os
import time
import psycopg2
import pytest
from fastapi.testclient import TestClient
from src.rest_api import app

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
    def publish(self, queue, msg): ...
    def consume(self, queue, timeout=5): ...
  return RabbitMQTestClient()

@pytest.fixture(scope="session")
def api_client():
  return TestClient(app)
