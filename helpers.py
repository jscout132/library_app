from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal

from models import User, Librarian

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        id = None

        if 'x-access-token' in request.headers:
            id=request.headers['x-access-token'].split(' ')[1]

        if not id:
            return jsonify({'message': 'token is missing'}), 401
        
        try:
            current_user_token = Librarian.query.filter_by(id = id).first()
        except:
            owner = Librarian.query.filter_by(id = id).first()

            if id != owner.id and secrets.compare_digest(id, owner.id):
                return jsonify({'message':'lib id is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated



class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)