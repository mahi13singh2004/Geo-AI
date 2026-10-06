from app.processors.kml_processor import KMLProcessor
from app.processors.shapefile_processor import ShapefileProcessor
from app.processors.base import GeoFileProcessor


class ProcessorFactory:
    @staticmethod
    def get_processor(file_extension: str) -> GeoFileProcessor:
        if file_extension == ".kml":
            return KMLProcessor()
        elif file_extension == ".zip":
            return ShapefileProcessor()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
