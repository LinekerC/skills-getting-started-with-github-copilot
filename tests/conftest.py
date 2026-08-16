"""
Shared pytest fixtures for API tests.
"""
import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provides a FastAPI TestClient for making requests to the app.
    """
    return TestClient(app)


@pytest.fixture
def test_activities_data():
    """
    Provides a deep copy of the activities data to isolate tests.
    This ensures tests don't mutate the global activities state.
    """
    return copy.deepcopy(activities)


@pytest.fixture
def reset_activities(monkeypatch, test_activities_data):
    """
    Patches the global activities dict with test data for each test.
    Automatically resets after each test.
    """
    monkeypatch.setattr("src.app.activities", test_activities_data)
    return test_activities_data
