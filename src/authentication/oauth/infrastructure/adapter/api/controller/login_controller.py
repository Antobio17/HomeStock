from flask import url_for
from src.oauth import google

class LoginController:
    
    @staticmethod
    def __invoke__():
        return google.authorize_redirect(
            url_for('authentication_oauth_authorize.__invoke__', _external=True)
        )
    