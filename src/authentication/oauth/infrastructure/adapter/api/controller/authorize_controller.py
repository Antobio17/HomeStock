from flask import jsonify # type: ignore
from src.oauth import google
from datetime import datetime, timezone
from src.authentication.user.infrastructure.domain.service.sqlalchemy.initialize_user_schema import InitializeUserSchema

class AuthorizeController:
    
    def __invoke__(self):
        response = google.authorize_access_token()

        try:
            InitializeUserSchema(
                response['userinfo']['sub'],
                response['userinfo']['email']
            ).execute()
        except Exception as e:
            return jsonify(
                {
                    'errors': [
                        {
                            'status': 500,
                            'title': 'An error occurred while initializing the user schema',
                            'details': str(e)
                        }
                    ]
                }
            ), 500
            
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
                'expired_at':  datetime.fromtimestamp(response['expires_at'], timezone.utc).isoformat(),
                'expires_in': response['expires_in']               
            }
        ), 202
