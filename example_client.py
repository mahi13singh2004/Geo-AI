import requests
import json
import sys


BASE_URL = "http://localhost:8000"


def upload_file(file_path):
    print(f"\nUploading file: {file_path}")
    with open(file_path, "rb") as f:
        response = requests.post(f"{BASE_URL}/api/v1/files/", files={"file": f})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Upload successful!")
        print(f"  File ID: {data['id']}")
        print(f"  Status: {data['status']}")
        return data["id"]
    else:
        print(f"✗ Upload failed: {response.status_code}")
        print(f"  Error: {response.text}")
        return None


def get_file_info(file_id):
    print(f"\nGetting file info for: {file_id}")
    response = requests.get(f"{BASE_URL}/api/v1/files/{file_id}/")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ File info retrieved:")
        print(f"  Filename: {data['filename']}")
        print(f"  Feature Count: {data['feature_count']}")
        print(f"  CRS: {data['crs']}")
        print(f"  Status: {data['status']}")
        print(f"  File Size: {data['file_size']} bytes")
        return data
    else:
        print(f"✗ Failed to get file info: {response.status_code}")
        return None


def get_measurements(file_id, page=1, limit=10):
    print(f"\nGetting measurements for: {file_id}")
    response = requests.get(
        f"{BASE_URL}/api/v1/files/{file_id}/measurements/",
        params={"page": page, "limit": limit}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Measurements retrieved:")
        print(f"  Total Features: {data['total']}")
        print(f"  Page: {data['page']}/{(data['total'] + data['limit'] - 1) // data['limit']}")
        print(f"\n  Features:")
        for feature in data["results"]:
            print(f"    Feature {feature['feature_id']}: {feature['geometry_type']}")
            if feature["measurement"]:
                m = feature["measurement"]
                print(f"      → {m['type']}: {m['value']:.2f} {m['unit']}")
            else:
                print(f"      → {feature['measurement_status']}")
        return data
    else:
        print(f"✗ Failed to get measurements: {response.status_code}")
        return None


def check_health():
    print("Checking API health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ API is healthy and running")
            return True
        else:
            print("✗ API is not responding correctly")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API. Is it running?")
        print(f"  Make sure the server is running at {BASE_URL}")
        return False


def main():
    print("=" * 60)
    print("Geospatial File Measurement API - Example Client")
    print("=" * 60)
    
    if not check_health():
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("\nUsage: python example_client.py <file_path>")
        print("Example: python example_client.py tests/fixtures/sample_polygon.kml")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    file_id = upload_file(file_path)
    if not file_id:
        sys.exit(1)
    
    get_file_info(file_id)
    get_measurements(file_id)
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
