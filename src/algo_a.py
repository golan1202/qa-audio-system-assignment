class AlgoA:
    @staticmethod
    def process(data: dict) -> dict:
        """
        Expects: {"sensor_id": int, "value": float}
        Returns: {"sensor_id": int, "processed": float}
        """
        value = data["value"]
        processed = value * 2

        return {
            "sensor_id": data["sensor_id"],
            "processed": processed
        }
