import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module

ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities(monkeypatch):
    fresh_state = copy.deepcopy(ORIGINAL_ACTIVITIES)
    monkeypatch.setattr(app_module, "activities", fresh_state)


@pytest.fixture
def client():
    return TestClient(app_module.app)
