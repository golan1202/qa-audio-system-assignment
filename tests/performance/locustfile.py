from locust import HttpUser, task, between

class RestApiUser(HttpUser):
    wait_time = between(0.1, 1.0)

    @task
    def get_realtime_features(self):
        self.client.get("/features/realtime?sensor_id=s1")
