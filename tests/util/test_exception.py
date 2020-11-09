import json

from werkzeug.datastructures import Headers
from werkzeug.exceptions import Unauthorized
from rfidsecuritysvc.util import exception

def test_render_unauthorized():
    e = Unauthorized(description='Test')
    r = exception.render_unauthorized(e)

    expected_response = {
        'title': 'Unauthorized',
        'status': 401,
        'detail': e.description,
    }
    assert len(r.response) == 1
    assert expected_response == json.loads(r.response[0])
    assert r.status_code == 401
    assert r.mimetype == 'application/json'
    assert r.content_type == 'application/json'
    expected_headers = Headers({'WWW_Authenticate': 'OAuth realm="rfid-security-svc API"', 'Content-Type': 'application/json', 'Content-Length': '58'})
    assert r.headers == expected_headers

