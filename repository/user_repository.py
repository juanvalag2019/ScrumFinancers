from models import User
from mongoengine.errors import ValidationError,NotUniqueError

class UserRepository:
    def save_user(self, user):
        try:
            user.validate()
            user.save()
        except (ValidationError,NotUniqueError):
            return None
        return user

user_repository = UserRepository()