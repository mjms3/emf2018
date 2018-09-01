import http

from flask.json import jsonify
from logging import getLogger

_log = getLogger('endpoints')

def _success_response(result):
    if result is None:
        resp = jsonify(success=True)
    else:
        resp = jsonify(success=True, value=result)
    resp.status_code = http.HTTPStatus.OK
    return resp


def _error_response(msg):
    resp = jsonify(success=False, error=msg)
    resp.status_code = http.HTTPStatus.BAD_REQUEST
    return resp

def _apply_end_point(func, arg):
    try:
        error_message, result = func(arg)
        if error_message is None:
            return _success_response(result)
        elif isinstance(error_message,str):
            return _error_response(error_message)
        else:
            raise ValueError(f'Unexpected return value: {error_message}')
    except Exception:
        _log.exception("Failed execute end point with error:\n")
