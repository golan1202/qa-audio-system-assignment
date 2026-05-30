import threading
import time

class QueueConsumer:
    def __init__(self, rabbitmq_client, data_writer, queue_name):
        self.rabbitmq = rabbitmq_client
        self.writer = data_writer
        self.queue = queue_name
        self.running = False

    def start(self):
        self.running = True
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()

    def run(self):
        while self.running:
            msg = self.rabbitmq.consume(self.queue)
            if msg:
                self.writer.write(msg)
            time.sleep(0.1)

    def stop(self):
        self.running = False
