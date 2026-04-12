import pytest
from typing import Any, Callable, Mapping
from rfidsecuritysvc.model.base_model import BaseModel
from rfidsecuritysvc.model.media import Media
from rfidsecuritysvc.model.permission import Permission

@pytest.fixture(scope='session')
def open_door(open_door_media: Media, open_door_permission: Permission) -> tuple[Media, Permission]:
    """
    This fixture returns a tuple containing the Media and Permission objects corresponding to the open door test
    data
    """
    return (open_door_media, open_door_permission)


@pytest.fixture(scope='session')
def assert_model() -> Callable[[Any, Any], None]:
    def go(expected: Any, actual: Any) -> None:
        if isinstance(expected, BaseModel):
            expected = expected.to_json()
        if isinstance(actual, BaseModel):
            actual = actual.to_json()
        _assert_keys(expected, actual)
        _assert_keys(actual, expected)

    return go


def _assert_keys(one: Mapping[str, Any], two: Mapping[str, Any]) -> None:
    for k, v in one.items():
        assert k in two
        assert two[k] == v
