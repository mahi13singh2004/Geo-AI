from abc import ABC, abstractmethod
from typing import List, Dict, Any


class GeoFileProcessor(ABC):
    @abstractmethod
    def process(self, file_path: str) -> Dict[str, Any]:
        pass
