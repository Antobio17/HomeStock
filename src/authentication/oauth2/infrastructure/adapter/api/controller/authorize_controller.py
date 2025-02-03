from src.config import google
from flask import Blueprint, jsonify # type: ignore

class AuthorizeController:
    def __init__(self):
        self.main = Blueprint('authorize', __name__)
        self.main.add_url_rule('/v1/authorize', view_func = self.__invoke__, methods = ['GET'])    
    
    def __invoke__(self):
        token = google.authorize_access_token()
        return jsonify(token)