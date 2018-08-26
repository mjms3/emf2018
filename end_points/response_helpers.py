import http

from flask.json import jsonify


def _success_response():
    resp = jsonify(success=True)
    resp.status_code = http.HTTPStatus.OK
    return resp


def _error_response(msg):
    resp = jsonify(success=False, error=msg)
    resp.status_code = http.HTTPStatus.BAD_REQUEST
    return resp

