import json
from flask import Response
def render_unauthorized(e):
    obj=json.dumps({
        'title': 'Unauthorized',
        'status': 401,
        'detail': e.description,
    })
    return Response(
        response=obj,
        status=401,
        mimetype='application/json',
        content_type='application/json',
        headers={'WWW_Authenticate': 'OAuth realm="rfid-security-svc API"'}
    )
