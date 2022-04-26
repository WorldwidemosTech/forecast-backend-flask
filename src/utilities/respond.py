import json
from datetime import datetime
from uuid import UUID

from flask import Response


def stringify_uuids(t: dict):
    """Replace all UUIDs in dictionary with UUID.hex (strings without dashes)"""
    return {n: (v.hex if isinstance(v, UUID)
                else stringify_uuids(v) if isinstance(v, dict)
    else [stringify_uuids(i) if isinstance(i, dict) else i for i in v] if isinstance(v, list)
    else str(v) if isinstance(v, datetime)
    else v) for n, v in t.items() if not n.startswith('_')}


def build_headers():
    return {
        'Content-Type': 'application/json',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'x-frame-options': 'deny',
        'X-XSS-Protection': '1; mode=block'
    }


def error(di_error: int, message: str, http_code: int, field: str = None, failed_field_value: list = None,
          x_origin=True):
    headers = build_headers()

    if x_origin and field is None:
        return Response(response=json.dumps({'success': False,
                                             'error_code': di_error,
                                             'error': message}, indent=4),
                        status=http_code,
                        headers=headers,
                        mimetype='application/json')
    else:
        return Response(response=json.dumps({'success': False,
                                             'error_code': di_error,
                                             'field': field,
                                             'failed_field_value': None if failed_field_value is None else
                                             failed_field_value,
                                             'error': message}, indent=4),
                        status=http_code,
                        headers=headers,
                        mimetype='application/json')


def success(message='', meta_info=''):
    headers = build_headers()
    if meta_info == '':
        response = {'success': True, 'message': message}
    else:
        response = {'success': True, 'message': message, 'meta': meta_info}
    if message == '':
        del response['message']
    #  response = stringify_uuids(response)
    return Response(response=json.dumps(response, indent=4),
                    status=200,
                    headers=headers,
                    mimetype='application/json')
