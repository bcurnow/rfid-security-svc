from connexion.context import request

from rfidsecuritysvc.model import sound as model


def get(name: str) -> dict | tuple[str, int, dict]:
    m = model.get_by_name(name)
    if m:
        # IOS (and maybe others) require that the server support Range requests
        # and the Content-Range header in order to play audio/video content
        content_length = len(m.content)
        range_header = request.headers.get('Range', '')

        if range_header:
            start, end = _parse_range(range_header, content_length)
            content_range = f'bytes {start}-{end - 1}/{content_length}'
            return m.content[start:end], 206, {'Content-Range': content_range}
        else:
            return m.content, 200, {'Content-Range': f'bytes 0-{content_length - 1}/{content_length}'}

    return f'Object with name "{name}" does not exist.', 404


def _parse_range(range_header: str, content_length: int) -> tuple[int, int]:
    """
    Parse a Range header value (e.g. 'bytes=0-1023') and return a
    half-open [start, end) interval suitable for slicing.
    """
    try:
        byte_range = range_header.strip().lower().removeprefix('bytes=')
        start_str, end_str = byte_range.split('-', 1)

        start = int(start_str) if start_str else None
        end = int(end_str) if end_str else None

        if start is None and end is None:
            raise ValueError('Empty range')
        elif start is None:
            # bytes=-500 → last 500 bytes
            start = max(content_length - end, 0)
            end = content_length
        elif end is None:
            # bytes=500- → from byte 500 to EOF
            end = content_length
        else:
            # bytes=0-999 → convert inclusive end to exclusive
            end = end + 1

        start = max(0, start)
        end = min(content_length, end)
        return start, end

    except (ValueError, AttributeError):
        # Malformed range — return full content bounds
        return 0, content_length
