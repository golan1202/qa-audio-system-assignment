from fastapi import FastAPI
from src.models import AudioEvent, AudioResponse
from src.algo_b import AlgoB
from src.data_writer import DataWriter

def create_app():
    app = FastAPI()

    algo = AlgoB()
    writer = DataWriter()

    @app.post("/realtime", response_model=AudioResponse)
    def realtime(event: AudioEvent, db_connection):
        processed = algo.process(event.model_dump())
        writer.write_feature_to_db(db_connection, processed)
        return {"status": "ok", "processed": processed["processed"]}

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
