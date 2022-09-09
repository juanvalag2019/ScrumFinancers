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

    def get_user_emails(self):
        try:
            return [user['email'] for user in User.objects]
        except (ValidationError,NotUniqueError):
            return []
user_repository = UserRepository()