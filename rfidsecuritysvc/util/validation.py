from rfidsecuritysvc.exception import InvalidValueError


def is_truthy(value):
    if not value:
        raise InvalidValueError()
    return True
