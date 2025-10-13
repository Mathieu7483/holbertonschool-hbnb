from hbnb.app.models.basemodel import BaseModel
import uuid
from datetime import datetime

class User(BaseModel):
    def __init__(self, id : str, first_name : str, last_name : str, email : str, is_admin :bool, created_at, updtaed_at):
        super().__init__()
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.created_at = created_at
        self.updated_at = updtaed_at
        self.users = [] #list to store related users

    def add_user(self, user):
        """Add a user to the place."""
        self.users.append(user)