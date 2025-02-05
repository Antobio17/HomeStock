from flask import url_for # type: ignore
from src.oauth import google

class LoginController:
    
    def __invoke__(self):
        return google.authorize_redirect(
            url_for('authentication_oauth_authorize.__invoke__', _external=True)
        )
    