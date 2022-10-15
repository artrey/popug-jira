import pytest

from scheme_registry import SchemeRegistry


@pytest.fixture
def scheme_registry():
    return SchemeRegistry()


def test_load_scheme__ok(scheme_registry):
    assert scheme_registry._load_scheme("auth.UserRegistered", 1) is not None


def test_load_scheme__no_file(scheme_registry):
    with pytest.raises(FileNotFoundError):
        scheme_registry._load_scheme("not.Found", 1)
