from locust import HttpUser, task, between, LoadTestShape
import json
import os
import random
import time


# ---------------------------------------------------------
#  CONFIGURATION
# ---------------------------------------------------------

API_BASE = os.getenv("API_BASE", "http://localhost:8000")
SENSOR_IDS = [1, 2, 3, 4, 5]


def generate_audio_payload():
    """Simulates a realistic audio event payload."""
    return {
        "sensor_id": random.choice(SENSOR_IDS),
        "value": random.randint(1, 100),
        "timestamp": int(time.time() * 1000),
    }


# ---------------------------------------------------------
#  USER BEHAVIOR: REAL-TIME API LOAD
# ---------------------------------------------------------

class RealTimeUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def send_realtime_event(self):
        payload = generate_audio_payload()
        with self.client.post(
            "/realtime",
            json=payload,
            name="POST /realtime",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status: {response.status_code}")
            else:
                response.success()


# ---------------------------------------------------------
#  USER BEHAVIOR: HISTORICAL API LOAD
# ---------------------------------------------------------

class HistoricalUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task
    def fetch_historical_data(self):
        sensor_id = random.choice(SENSOR_IDS)
        with self.client.get(
            f"{API_BASE}/historical?sensor_id={sensor_id}",
            name="GET /historical",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status: {response.status_code}")
            else:
                try:
                    data = response.json()
                    if not isinstance(data, list):
                        response.failure("Invalid response format")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON")
                response.success()


# ---------------------------------------------------------
#  USER BEHAVIOR: MIXED TRAFFIC (REALTIME + HISTORICAL)
# ---------------------------------------------------------

class MixedTrafficUser(HttpUser):
    wait_time = between(0.2, 1.0)

    @task(3)
    def realtime(self):
        payload = generate_audio_payload()
        self.client.post(f"{API_BASE}/realtime", json=payload, name="POST /realtime")

    @task(1)
    def historical(self):
        sensor_id = random.choice(SENSOR_IDS)
        self.client.get(f"{API_BASE}/historical?sensor_id={sensor_id}", name="GET /historical")


# ---------------------------------------------------------
#  OPTIONAL: RABBITMQ LOAD SIMULATION (IF API IS NOT USED)
# ---------------------------------------------------------

class RabbitMQUser(HttpUser):
    """
    This simulates direct queue load if developers expose a test endpoint
    like /test/publish for load testing RabbitMQ.
    """
    wait_time = between(0.05, 0.2)

    @task
    def publish_to_queue(self):
        payload = generate_audio_payload()
        self.client.post(f"{API_BASE}/test/publish", json=payload, name="POST /test/publish")


# ---------------------------------------------------------
#  CUSTOM LOAD SHAPE (OPTIONAL)
# ---------------------------------------------------------

class StepLoadShape(LoadTestShape):
    """
    Gradually increases load in steps:
    - Start at 10 users
    - Increase by +10 every minute
    - Max 100 users
    """

    step_time = 60
    step_load = 10
    max_users = 100

    def tick(self):
        run_time = self.get_run_time()

        current_step = int(run_time / self.step_time)
        user_count = min(current_step * self.step_load, self.max_users)

        if user_count > self.max_users:
            return None

        return user_count, user_count
