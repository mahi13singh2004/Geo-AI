import geopandas as gpd
import zipfile
import os
import tempfile
from app.processors.base import GeoFileProcessor
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class ShapefileProcessor(GeoFileProcessor):
    def process(self, file_path: str) -> Dict[str, Any]:
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    zip_ref.extractall(temp_dir)

                shp_file = None
                for file in os.listdir(temp_dir):
                    if file.endswith(".shp"):
                        shp_file = os.path.join(temp_dir, file)
                        break

                if not shp_file:
                    raise ValueError("No .shp file found in ZIP archive")

                gdf = gpd.read_file(shp_file)

                features = []
                for idx, row in gdf.iterrows():
                    feature = {
                        "index": idx,
                        "geometry": row.geometry,
                        "geometry_type": (
                            row.geometry.geom_type if row.geometry else None
                        ),
                        "properties": row.drop("geometry").to_dict(),
                        "crs": str(gdf.crs) if gdf.crs else None,
                    }
                    features.append(feature)

                return {
                    "features": features,
                    "crs": str(gdf.crs) if gdf.crs else None,
                    "feature_count": len(features),
                }
        except Exception as e:
            logger.error(f"Shapefile processing failed: {str(e)}")
            raise
