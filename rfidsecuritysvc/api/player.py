from flask import request

from rfidsecuritysvc.model import sound as model


def get(name):
    m = model.get(name)
    if m:
        # IOS (and maybe others) require that the server support Range requests
        # and the Content-Range header in order to play audio/video content
        content_length = len(m.content)
        if request.range:
            start, end = request.range.range_for_length(content_length)

            return m.content[start:end], 206, {'Content-Range': request.range.to_content_range_header(content_length)}
        else:
            return m.content, 200, {'Content-Range': f'bytes 0-{content_length}/{content_length}'}

    return f'Object with name "{name}" does not exist.', 404
