import pytest
from app.utils.file_validation import validate_file_extension, validate_file_size


def test_validate_kml_extension():
    is_valid, ext = validate_file_extension("test.kml")
    assert is_valid == True
    assert ext == ".kml"


def test_validate_zip_extension():
    is_valid, ext = validate_file_extension("test.zip")
    assert is_valid == True
    assert ext == ".zip"


def test_validate_invalid_extension():
    is_valid, error = validate_file_extension("test.txt")
    assert is_valid == False
    assert error == "UNSUPPORTED_FILE_TYPE"


def test_validate_file_size_valid():
    is_valid, error = validate_file_size(1024)
    assert is_valid == True


def test_validate_file_size_too_large():
    is_valid, error = validate_file_size(100 * 1024 * 1024)
    assert is_valid == False
    assert error == "FILE_TOO_LARGE"
