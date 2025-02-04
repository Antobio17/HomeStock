from src.oauth import google
from flask import Blueprint, jsonify # type: ignore
from datetime import datetime, timezone

class AuthorizeController:
    def __init__(self):
        self.main = Blueprint('authorize', __name__)
        self.main.add_url_rule('/v1/authorize', view_func = self.__invoke__, methods = ['GET'])    
    
    def __invoke__(self):
        response = google.authorize_access_token()
        expired_at = datetime.fromtimestamp(response['expires_at'], timezone.utc).isoformat()

        return jsonify(
            {
                'userinfo': {
                    'email': response['userinfo']['email'],
                    'given_name': response['userinfo']['given_name'],
                    'family_name': response['userinfo']['family_name'],
                    'picture': response['userinfo']['picture'],
                    'email_verified': response['userinfo']['email_verified']
                },
                'token_type': response['token_type'],
                'token': response['id_token'],
                'expired_at': expired_at,
                'expires_in': response['expires_in']               
            }
        ), 202
