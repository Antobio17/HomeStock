from src.config import google
from flask import Blueprint, url_for # type: ignore

class LoginController:
    def __init__(self):
        self.main = Blueprint('login', __name__)
        self.main.add_url_rule('/v1/login', view_func = self.__invoke__, methods = ['GET'])    
    
    def __invoke__(self):
        return google.authorize_redirect(url_for('authorize.__invoke__', _external=True))
    