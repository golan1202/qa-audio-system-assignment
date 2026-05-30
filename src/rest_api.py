from fastapi import FastAPI, Depends

from src.algo_a import AlgoA
from src.models import AudioEvent, AudioResponse
from src.algo_b import AlgoB
from src.data_writer import DataWriter
from src.rabbitmq_client import RabbitMQClient


def get_rabbitmq_client():
    return RabbitMQClient()

def create_app():
    app = FastAPI()

    algo_a = AlgoA()
    algo_b = AlgoB()
    writer = DataWriter()

    @app.post("/realtime", response_model=AudioResponse)
    def realtime(
        event: AudioEvent,
        db_connection, rabbitmq = Depends(get_rabbitmq_client)
    ):
        if event.algorithm == "A":
            processed = algo_a.process(event.model_dump())
        else:
            processed = algo_b.process(event.model_dump())
        writer.write(db_connection, processed)

        # publish to queue
        rabbitmq.publish("audio_events", processed)

        return {"status": "ok", "processed": processed["processed"]}

    return app