from fastapi import FastAPI

from src.algo_a import AlgoA
from src.models import AudioEvent, AudioResponse
from src.algo_b import AlgoB
from src.data_writer import DataWriter

def create_app():
    app = FastAPI()

    algo_a = AlgoA()
    algo_b = AlgoB()
    writer = DataWriter()

    @app.post("/realtime", response_model=AudioResponse)
    def realtime(event: AudioEvent, db_connection):
        if event.algorithm == "A":
            processed = algo_a.process(event.model_dump())
        else:
            processed = algo_b.process(event.model_dump())

        writer.write_feature_to_db(db_connection, processed)
        return {"status": "ok", "processed": processed["processed"]}


    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
