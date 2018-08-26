import http

import json


def _success_response():
    return {
        'statusCode': http.HTTPStatus.OK,
        'headers': {
            'Content-Type': 'application/json',
        }
    }


def _error_response(msg):
    return {
        'statusCode': http.HTTPStatus.BAD_REQUEST,
        'body': json.dumps({'error': msg}),
        'headers': {
            'Content-Type': 'application/json',
        }
    }

