from rfidsecuritysvc.model import sound as model


def get(name):
    m = model.get(name)
    if m:
        return m.content

    return f'Object with name "{name}" does not exist.', 404
