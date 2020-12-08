import pytest

from rfidsecuritysvc.exception import InvalidValueError
from rfidsecuritysvc.util.validation import is_truthy


def test_is_truthy():
    assert is_truthy(True)
    assert is_truthy('Some Value')
    assert is_truthy([None])
    assert is_truthy({'key': None})

def test_is_truthy_False():
    with pytest.raises(InvalidValueError):
        assert not is_truthy(None)
    with pytest.raises(InvalidValueError):
        assert not is_truthy('')
    with pytest.raises(InvalidValueError):
        assert not is_truthy([])
    with pytest.raises(InvalidValueError):
        assert not is_truthy({})
