import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture
def client():
    """Provide a TestClient and restore in-memory activities after each test.

    Uses deepcopy to snapshot the `activities` dict then restores it in-place
    so the running app keeps the same object identity.
    """
    original = copy.deepcopy(app_module.activities)
    with TestClient(app_module.app) as c:
        yield c

    # restore original data in-place
    app_module.activities.clear()
    app_module.activities.update(original)
