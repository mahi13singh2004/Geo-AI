import geopandas as gpd
from app.processors.base import GeoFileProcessor
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class KMLProcessor(GeoFileProcessor):
    def process(self, file_path: str) -> Dict[str, Any]:
        try:
            gdf = gpd.read_file(file_path, driver="KML")
            
            features = []
            for idx, row in gdf.iterrows():
                feature = {
                    "index": idx,
                    "geometry": row.geometry,
                    "geometry_type": row.geometry.geom_type if row.geometry else None,
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
            logger.error(f"KML processing failed: {str(e)}")
            raise
