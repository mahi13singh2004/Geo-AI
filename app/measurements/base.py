from abc import ABC, abstractmethod
from shapely.geometry.base import BaseGeometry
from typing import Optional, Tuple


class MeasurementStrategy(ABC):
    @abstractmethod
    def calculate(
        self, geometry: BaseGeometry
    ) -> Tuple[Optional[float], Optional[str], str]:
        pass
