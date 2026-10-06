from typing import Optional


class Measurement:
    def __init__(
        self,
        measurement_type: Optional[str],
        value: Optional[float],
        unit: Optional[str],
        status: str = "COMPLETED",
    ):
        self.measurement_type = measurement_type
        self.value = value
        self.unit = unit
        self.status = status
