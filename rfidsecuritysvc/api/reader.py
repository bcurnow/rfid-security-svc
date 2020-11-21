from rfidsecuritysvc.model import reader


def search(timeout=10):
    return reader.read(timeout)
