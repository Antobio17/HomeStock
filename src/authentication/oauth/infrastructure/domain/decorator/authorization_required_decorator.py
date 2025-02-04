import json
from functools import wraps
from google.auth import jwt # type: ignore
from flask import request, jsonify # type: ignore

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify(
                {
                    'errors': [
                        {
                            'status': 401,
                            'title': 'Bearer Token is required',
                            'details': 
                                'A Bearer Token is required to access this resource. '
                                'It must be included in the Authorization header.'
                        }
                    ]
                }
            ), 401

        try:
            with open('/app/conf/security/certs.json', 'r') as certs_file:
                certs = json.load(certs_file)
            claims = jwt.decode(token[len('Bearer '):], certs = certs, verify = True)
        except Exception as e:
            return jsonify(
                {
                    'errors': [
                        {
                            'status': 401,
                            'title': 'Token is invalid',
                            'details': str(e)
                        }
                    ]
                }
            ), 401
            
        # TODO check if the user exists. Study if database is needed.
        
        return f(*args, **kwargs)
    
    return decorated