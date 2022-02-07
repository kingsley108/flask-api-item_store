from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    print(username)
    user = UserModel.verify_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.verify_by_id(user_id)