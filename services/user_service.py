from models import User
from repository.user_repository import user_repository

class UserService : 
    def create_user(self,email):
        user=User(email=email)
        return user_repository.save_user(user)

user_service=UserService()