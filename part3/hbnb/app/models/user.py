from app.models.basemodel import BaseModel
from app.extensions import db, bcrypt


class User(BaseModel):
    """
    Represents a user in the HBnB application.

    Inherits:
        BaseModel: Provides id, created_at, and updated_at.
    """

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        """
        Initialize a new User instance with validation.
        """
        super().__init__()

        if len(first_name) > 50:
            raise ValueError(
                "Your first name must have less than 50 characters"
            )
        self.first_name = first_name

        if len(last_name) > 50:
            raise ValueError(
                "Your last name must have less than 50 characters"
            )
        self.last_name = last_name

        if '@' not in email:
            raise TypeError(
                "Enter a valid address, e.g. example@gmail.com"
            )
        self.email = email

        self.is_admin = is_admin

        if password:
            self.hash_password(password)

    def to_dict(self):
        """
        Serialize the user to a dictionary, excluding sensitive fields
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password.encode('utf-8'), password)
