from typing import List
from app.processors.factory import ProcessorFactory
from app.services.measurement_service import MeasurementService
from app.models.feature import FeatureModel
from app.utils.geometry import validate_geometry
import logging

logger = logging.getLogger(__name__)


class ProcessingService:
    def __init__(self):
        self.measurement_service = MeasurementService()

    def process_file(self, file_path: str, file_id: str, file_type: str) -> List[FeatureModel]:
        processor = ProcessorFactory.get_processor(file_type)
        result = processor.process(file_path)

        features = []
        for feature_data in result["features"]:
            geometry = feature_data["geometry"]
            geometry_type = feature_data["geometry_type"]
            
            if not geometry or not validate_geometry(geometry):
                feature_model = FeatureModel(
                    id=None,
                    file_id=file_id,
                    feature_index=feature_data["index"],
                    geometry_type=geometry_type or "Unknown",
                    geometry=str(geometry) if geometry else "",
                    properties=feature_data.get("properties"),
                    source_crs=feature_data.get("crs"),
                    measurement_crs=None,
                    measurement_type=None,
                    measurement_value=None,
                    measurement_unit=None,
                    measurement_status="INVALID_GEOMETRY",
                )
            else:
                measurement = self.measurement_service.calculate_measurement(
                    geometry, feature_data["crs"], geometry_type
                )
                
                feature_model = FeatureModel(
                    id=None,
                    file_id=file_id,
                    feature_index=feature_data["index"],
                    geometry_type=geometry_type,
                    geometry=geometry.wkt,
                    properties=feature_data.get("properties"),
                    source_crs=feature_data.get("crs"),
                    measurement_crs=feature_data.get("crs"),
                    measurement_type=measurement.measurement_type,
                    measurement_value=measurement.value,
                    measurement_unit=measurement.unit,
                    measurement_status=measurement.status,
                )
            
            features.append(feature_model)

        return features
