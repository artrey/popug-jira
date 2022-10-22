import datetime as dt

import pytest

from scheme_registry import SchemeRegistry


@pytest.fixture
def scheme_registry():
    return SchemeRegistry()


def test_load_scheme__ok(scheme_registry):
    assert scheme_registry._load_scheme("auth.UserCreated", 1) is not None


def test_load_scheme__no_file(scheme_registry):
    with pytest.raises(FileNotFoundError):
        scheme_registry._load_scheme("not.Found", 1)


def test_validate(scheme_registry):
    event_data = {
        "event_id": "08627d5a-2cc7-402f-bd34-107e4dad675c",
        "event_name": "task_tracker.TaskCreated",
        "event_version": 2,
        "event_time": dt.datetime.fromisoformat("2022-10-16T15:39:08.158348"),
        "producer": "popug-jira-task-tracker",
        "data": {
            "public_id": "24c1bb13-26a2-42f9-a716-2420d1051697",
            "title": "some title",
            "jira_id": "some-id",
            "status": "В работе",
            "executor_public_id": "9dcea011-d424-47de-96d1-dd08096590a9",
        },
    }
    assert scheme_registry.validate_event(event_data, "task_tracker.TaskCreated", 2) is True

    event_data["data"]["title"] = "[APP-100] some task"
    assert scheme_registry.validate_event(event_data, "task_tracker.TaskCreated", 2) is False
