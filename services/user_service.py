from models import User
from repository.user_repository import user_repository

class UserService : 
    def create_user(self,email):
        user=User(email=email)
        return user_repository.save_user(user)

    def send_email_updates(self, updates):
        pass

user_service=UserService()