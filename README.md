# Geospatial File Measurement API

A production-quality FastAPI backend for processing geospatial files and calculating accurate measurements with automatic coordinate reference system handling.

## Table of Contents
- [Features](#features)
- [Requirements Met](#requirements-met)
- [Additional Features](#additional-features-beyond-requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Architecture](#architecture)
- [Design Decisions](#design-decisions)
- [Learning](#learning)
- [Future Scope](#future-scope)

---

## Features

- Upload and process KML and Shapefile (ZIP) formats
- Automatic CRS detection and transformation
- Accurate area calculation for Polygons (m²)
- Accurate length calculation for LineStrings (m)
- Geographic to projected coordinate transformation
- Geometry validation with graceful error handling
- REST API with interactive documentation

---

## Requirements Met

### 1. Backend Framework ✅
**FastAPI** - Modern, fast web framework with automatic API documentation

### 2. File Upload ✅
**POST /api/v1/files/**
- Accepts `.kml` files
- Accepts `.zip` containing Shapefiles
- Validates file type and size
- Returns file ID and processing status

### 3. File Processing ✅
Extracts for every feature:
- Feature ID/index
- Geometry type
- Geometry coordinates
- CRS information
- Properties/attributes

Handles unsupported geometries gracefully without crashing.

### 4. Measurements ✅
- **Polygon**: Calculates area in m²
- **LineString**: Calculates length in m
- **Point**: No measurement (handled gracefully)

### 5. CRS Handling ✅ **CRITICAL**
**Does NOT calculate directly on lat/lon degrees**

The application correctly handles geographic coordinates (EPSG:4326):
1. Detects if CRS is geographic
2. Calculates geometry centroid
3. Determines appropriate UTM zone
4. Transforms geometry to projected CRS
5. Calculates measurement on projected coordinates
6. Returns results in meters/square meters

**Implementation:**
```python
# app/services/crs_service.py
if self.crs_service.is_geographic(crs):
    centroid = geometry.centroid
    utm_epsg = self.crs_service.determine_utm_zone(centroid.x, centroid.y)
    transformer = Transformer.from_crs(crs, utm_epsg, always_xy=True)
    projected_geom = transform(transformer.transform, geometry)
```

### 6. API Design ✅

**Upload:**
```http
POST /api/v1/files/
```

**File Information:**
```http
GET /api/v1/files/{id}/
```
Returns:
```json
{
    "id": "abc123",
    "filename": "survey.kml",
    "feature_count": 120,
    "crs": "EPSG:4326",
    "status": "COMPLETED"
}
```

**Measurements:**
```http
GET /api/v1/files/{id}/measurements/
```
Returns:
```json
{
    "file_id": "abc123",
    "page": 1,
    "limit": 100,
    "total": 120,
    "results": [
        {
            "feature_id": 0,
            "geometry_type": "Polygon",
            "measurement": {
                "type": "area",
                "value": 15234.52,
                "unit": "m²"
            },
            "measurement_status": "COMPLETED"
        }
    ]
}
```

### 7. Documentation ✅
This README includes:
- Setup instructions
- API documentation with examples
- Architecture explanation
- File processing flow
- Measurement calculation flow
- CRS handling strategy
- Design decisions and alternatives

---

## Additional Features (Beyond Requirements)

### Enhanced Functionality
- **Pagination Support**: Handle large datasets efficiently with page/limit parameters
- **Duplicate Detection**: SHA-256 hashing prevents reprocessing identical files
- **Multiple Geometry Types**: Support for MultiPolygon, MultiLineString
- **Health Check Endpoint**: `/health` for monitoring
- **Interactive Documentation**: Auto-generated Swagger UI at `/docs`

### Code Quality
- **Clean Architecture**: Separation of concerns with distinct layers
- **Design Patterns**: Factory, Strategy, and Repository patterns
- **Type Hints**: Complete type annotations throughout
- **Comprehensive Testing**: Unit and integration tests with pytest
- **Error Handling**: Consistent error responses with appropriate HTTP status codes
- **Structured Logging**: Production-ready logging for debugging

### Database
- **SQLite Persistence**: Stores files and features for retrieval
- **Repository Pattern**: Database abstraction for easy migration to PostgreSQL

### Developer Experience
- **Example Client**: Python script demonstrating API usage
- **Test Fixtures**: Sample KML files for immediate testing
- **Environment Configuration**: Easy configuration via .env file

---

## Installation

### Prerequisites
- Python 3.11 or higher
- pip

### Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd geospatial-measurement-api
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create uploads directory**
```bash
mkdir uploads
```

4. **Configure environment (optional)**
```bash
cp .env.example .env
```

---

## Running the Application

Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

---

## API Documentation

### Interactive Documentation
Visit **http://127.0.0.1:8000/docs** for Swagger UI

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
    "status": "healthy"
}
```

#### 2. Upload File
```http
POST /api/v1/files/
Content-Type: multipart/form-data
```

**Parameters:**
- `file`: The KML or ZIP file to upload

**Example (curl):**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/files/ \
  -F "file=@survey.kml"
```

**Response:**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "filename": "survey.kml",
    "status": "COMPLETED",
    "cached": false
}
```

#### 3. Get File Information
```http
GET /api/v1/files/{file_id}/
```

**Response:**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "filename": "survey.kml",
    "feature_count": 120,
    "crs": "EPSG:4326",
    "status": "COMPLETED",
    "file_size": 15234,
    "created_at": "2024-01-01T12:00:00"
}
```

#### 4. Get Measurements
```http
GET /api/v1/files/{file_id}/measurements/?page=1&limit=100
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Results per page (default: 100, max: 1000)

**Response:**
```json
{
    "file_id": "550e8400-e29b-41d4-a716-446655440000",
    "page": 1,
    "limit": 100,
    "total": 120,
    "results": [
        {
            "feature_id": 0,
            "geometry_type": "Polygon",
            "measurement": {
                "type": "area",
                "value": 123456.78,
                "unit": "m²"
            },
            "measurement_status": "COMPLETED"
        },
        {
            "feature_id": 1,
            "geometry_type": "LineString",
            "measurement": {
                "type": "length",
                "value": 842.31,
                "unit": "m"
            },
            "measurement_status": "COMPLETED"
        },
        {
            "feature_id": 2,
            "geometry_type": "Point",
            "measurement": null,
            "measurement_status": "NOT_REQUIRED"
        }
    ]
}
```

**Measurement Status Values:**
- `COMPLETED`: Measurement calculated successfully
- `NOT_REQUIRED`: Point geometry (no measurement needed)
- `NOT_SUPPORTED`: Unsupported geometry type
- `INVALID_GEOMETRY`: Geometry validation failed
- `CRS_UNKNOWN`: Missing CRS information
- `CALCULATION_FAILED`: Error during calculation

---

## Testing

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=app tests/
```

### Test with Example Client
```bash
python example_client.py tests/fixtures/sample_polygon.kml
```

### Manual Testing via Browser
1. Start the server: `uvicorn app.main:app --reload`
2. Visit: http://127.0.0.1:8000/docs
3. Use the interactive UI to test endpoints

### Example Python Test
```python
import requests

# Upload file
with open("tests/fixtures/sample_polygon.kml", "rb") as f:
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/files/",
        files={"file": f}
    )
file_id = response.json()["id"]

# Get measurements
measurements = requests.get(
    f"http://127.0.0.1:8000/api/v1/files/{file_id}/measurements/"
).json()

print(f"Features: {measurements['total']}")
for result in measurements["results"]:
    if result["measurement"]:
        m = result["measurement"]
        print(f"{result['geometry_type']}: {m['value']:.2f} {m['unit']}")
```

---

## Architecture

### Project Structure
```
geospatial-measurement-api/
├── app/
│   ├── main.py                      # FastAPI application entry point
│   ├── api/routes/                  # API endpoints
│   │   ├── files.py                 # File upload endpoint
│   │   └── measurements.py          # Measurements endpoint
│   ├── core/                        # Configuration & logging
│   │   ├── config.py
│   │   └── logging.py
│   ├── models/                      # Data models
│   │   ├── file.py
│   │   ├── feature.py
│   │   └── measurement.py
│   ├── schemas/                     # Pydantic validation schemas
│   │   ├── file.py
│   │   ├── feature.py
│   │   └── measurement.py
│   ├── services/                    # Business logic layer
│   │   ├── file_service.py          # File handling
│   │   ├── processing_service.py    # Feature extraction
│   │   ├── measurement_service.py   # Measurement calculation
│   │   └── crs_service.py           # CRS detection & transformation
│   ├── processors/                  # File format processors
│   │   ├── base.py                  # Base processor interface
│   │   ├── factory.py               # Processor selection
│   │   ├── kml_processor.py         # KML file handling
│   │   └── shapefile_processor.py   # Shapefile handling
│   ├── measurements/                # Measurement strategies
│   │   ├── base.py                  # Base strategy interface
│   │   ├── polygon.py               # Polygon area calculation
│   │   ├── linestring.py            # LineString length calculation
│   │   └── registry.py              # Strategy registry
│   ├── repositories/                # Database layer
│   │   ├── file_repository.py       # File CRUD operations
│   │   └── feature_repository.py    # Feature CRUD operations
│   └── utils/                       # Helper functions
│       ├── file_validation.py
│       ├── geometry.py
│       └── hashing.py
├── tests/
│   ├── unit/                        # Unit tests
│   ├── integration/                 # API tests
│   └── fixtures/                    # Test data
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Architecture Layers
```
┌─────────────────────────────────────────┐
│         API Layer (FastAPI)             │
│  - Request validation                   │
│  - Response serialization               │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Service Layer                    │
│  - Business logic                       │
│  - Orchestration                        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Processing Layer                    │
│  - File format detection                │
│  - Feature extraction                   │
│  - CRS handling                         │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     Measurement Layer                    │
│  - Geometry validation                  │
│  - Measurement calculation              │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     Repository Layer                     │
│  - Database operations                  │
│  - Data persistence                     │
└─────────────────────────────────────────┘
```

### File Processing Flow
```
1. Upload Request
   └─> File Validation (type, size)
       └─> Hash Calculation
           └─> Duplicate Check
               └─> Save to Disk
                   └─> Database Record

2. Processing
   └─> Format Detection (.kml or .zip)
       └─> Processor Factory Selection
           └─> Feature Extraction (GeoPandas)
               └─> CRS Detection

3. Measurement Calculation
   └─> For Each Feature:
       └─> Geometry Validation
           └─> CRS Check (Geographic?)
               ├─> Yes: Transform to UTM
               └─> No: Use as-is
                   └─> Calculate Measurement
                       └─> Save to Database

4. Return Results
```

### Measurement Calculation Flow
```
Input: Geometry + CRS
   │
   ▼
Is CRS Geographic? (e.g., EPSG:4326)
   │
   ├─> YES ─> Calculate Centroid
   │          │
   │          ▼
   │       Determine UTM Zone
   │       (based on lon/lat)
   │          │
   │          ▼
   │       Transform Geometry
   │       (EPSG:4326 → UTM)
   │          │
   │          └───┐
   │              │
   └─> NO ───────►│
                  ▼
          Select Strategy
          (Polygon/LineString)
                  │
                  ▼
          Calculate Measurement
          (area m² / length m)
                  │
                  ▼
          Return Result + Unit
```

### CRS Handling Strategy

**Problem:** Geographic coordinates (EPSG:4326) use degrees, not meters. Calculating area/distance directly on degrees produces incorrect results.

**Solution:**
1. **Detection**: Check if CRS is geographic using PyProj
2. **Centroid**: Calculate geometry centroid to determine location
3. **UTM Selection**: Automatically determine appropriate UTM zone:
   - Zone = floor((longitude + 180) / 6) + 1
   - Northern hemisphere: EPSG:326XX
   - Southern hemisphere: EPSG:327XX
4. **Transformation**: Use PyProj to transform geometry to UTM
5. **Calculation**: Calculate measurements on projected coordinates

**Example:**
```
Input:  Polygon at (10.0°E, 50.0°N) in EPSG:4326
        ↓
Centroid: (10.05°E, 50.05°N)
        ↓
UTM Zone: Zone 32N → EPSG:32632
        ↓
Transform: Geometry now in meters
        ↓
Calculate: area = 123,456,789 m² ✓ (not 0.01 degrees ✗)
```

---

## Design Decisions

### 1. Factory Pattern for File Processors
**Decision:** Use Factory pattern to select KML vs Shapefile processor

**Alternatives Considered:**
- Single processor with format detection logic
- Separate endpoints for each format

**Reasoning:**
- Easy to add new formats (GeoJSON, GPX, etc.) without modifying existing code
- Keeps format-specific logic isolated
- Follows Open/Closed Principle

**Implementation:** `app/processors/factory.py`

### 2. Strategy Pattern for Measurements
**Decision:** Separate measurement classes for each geometry type

**Alternatives Considered:**
- Single calculation function with if/else chains
- Measurement logic in geometry classes

**Reasoning:**
- Each geometry type has unique calculation logic
- Easy to add new measurement types (perimeter, centroid, etc.)
- Testable in isolation

**Implementation:** `app/measurements/`

### 3. Repository Pattern for Database
**Decision:** Abstract database operations behind repository layer

**Alternatives Considered:**
- Direct database calls from service layer
- ORM like SQLAlchemy

**Reasoning:**
- Easy to swap SQLite for PostgreSQL/PostGIS later
- Testable with mock repositories
- Keeps SQL isolated from business logic

**Implementation:** `app/repositories/`

### 4. Synchronous Processing
**Decision:** Process files synchronously (no background jobs)

**Alternatives Considered:**
- Celery + Redis for async processing
- Thread pool for concurrent processing

**Reasoning:**
- Simpler architecture, easier to run and debug
- No external dependencies (Redis, RabbitMQ)
- Sufficient for demonstration and small-to-medium files
- Can be upgraded to async later without API changes

**Future:** Add Celery for production use with large files

### 5. SQLite Database
**Decision:** Use SQLite for data persistence

**Alternatives Considered:**
- PostgreSQL with PostGIS extension
- In-memory storage only
- NoSQL (MongoDB with geospatial indexes)

**Reasoning:**
- Zero configuration required
- File-based, no server setup
- Sufficient for demonstration
- Repository pattern makes migration to PostgreSQL straightforward

**Future:** PostgreSQL/PostGIS for production

### 6. Automatic UTM Zone Selection
**Decision:** Calculate UTM zone automatically from geometry centroid

**Alternatives Considered:**
- Fixed global projection (e.g., Web Mercator)
- User-specified target CRS
- Distance-based heuristics

**Reasoning:**
- UTM provides accurate measurements for local areas
- Automatic selection requires no user input
- Works correctly for geometries anywhere in the world
- Industry standard approach

---

## Learning

### Geospatial Concepts
- **CRS Fundamentals**: Understanding geographic vs projected coordinate systems
- **The Degree Problem**: Why calculating area/distance on lat/lon is incorrect
- **UTM Zones**: How UTM divides the world into 60 zones for accurate local measurements
- **Coordinate Transformations**: Using PyProj for CRS transformations
- **Geospatial Libraries**: Working with GeoPandas, Shapely, Fiona

### Backend Development
- **FastAPI**: Building modern APIs with automatic documentation
- **Clean Architecture**: Implementing layered architecture with separation of concerns
- **Design Patterns**: Applying Factory, Strategy, and Repository patterns appropriately
- **Error Handling**: Graceful degradation instead of system crashes
- **API Design**: RESTful principles, proper HTTP status codes, pagination

### Software Engineering
- **Type Safety**: Using Python type hints for better code quality
- **Testing**: Writing comprehensive unit and integration tests
- **Documentation**: Creating clear, useful documentation
- **File Handling**: Secure file upload, validation, and storage
- **Database Design**: Schema design for geospatial relationships

### Key Insights
1. **CRS is Critical**: Never assume coordinates are in meters - always check and transform
2. **Validation Matters**: Real-world files contain invalid/malformed data
3. **Architecture Enables Growth**: Clean separation makes features easy to add
4. **Tests Catch Bugs**: Edge cases appear when processing diverse geospatial files
5. **Documentation is Code**: Good docs make the difference between adoption and abandonment

---

## Future Scope

### Immediate Enhancements
- **PostgreSQL/PostGIS**: Migrate to PostGIS for advanced spatial queries and better performance
- **Async Processing**: Implement Celery + Redis for background processing of large files
- **Additional Formats**: Support GeoJSON, GPX, GeoPackage formats
- **More Measurements**: Add perimeter, centroid, bounding box calculations

### Advanced Features
- **Spatial Queries**: Intersection, buffer, union operations
- **Web Interface**: React/Vue.js frontend with map visualization using Leaflet/Mapbox
- **Authentication**: JWT-based authentication and API keys
- **Export Options**: Export results to CSV, Excel, GeoJSON, Shapefile
- **Batch Processing**: Upload and process multiple files simultaneously
- **WebSocket**: Real-time progress updates for long-running operations

### Production Readiness
- **Docker**: Containerization with Docker and Docker Compose
- **CI/CD**: Automated testing and deployment pipeline
- **Monitoring**: Prometheus + Grafana for metrics
- **Logging**: ELK stack for centralized logging
- **Caching**: Redis for frequently accessed data
- **Rate Limiting**: Protect API from abuse

### Enterprise Features
- **Multi-tenancy**: Support for organization accounts
- **RBAC**: Role-based access control
- **Audit Logs**: Track all operations for compliance
- **Cloud Storage**: S3/Azure Blob integration
- **Load Balancing**: Horizontal scaling with multiple instances

---

## Technology Stack

- **Backend**: FastAPI, Pydantic, Uvicorn
- **Geospatial**: GeoPandas, Shapely, PyProj, Fiona
- **Database**: SQLite
- **Testing**: Pytest, HTTPX
- **Documentation**: OpenAPI (Swagger/ReDoc)

---

## License

MIT License

---

## Contact

For questions or feedback, please open an issue on GitHub.
