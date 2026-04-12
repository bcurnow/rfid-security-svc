from rfidsecuritysvc.model import reader


def search(timeout: int = 10) -> tuple[str, int]:
    return reader.read(timeout)
