import pytest
import tempfile
from app.utils.hashing import calculate_file_hash


def test_calculate_file_hash():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content")
        temp_path = f.name
    
    hash1 = calculate_file_hash(temp_path)
    hash2 = calculate_file_hash(temp_path)
    
    assert hash1 == hash2
    assert len(hash1) == 64
