import os
from authlib.integrations.flask_client import OAuth # type: ignore

oauth = OAuth()
google = None

def init_oauth(app):
    global google
    oauth.init_app(app)

    google = oauth.register(
        name='google',
        client_id=os.getenv('OAUTH_GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('OAUTH_GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile',
        },
    )