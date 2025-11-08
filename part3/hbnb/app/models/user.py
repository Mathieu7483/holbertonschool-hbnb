from app.models.basemodel import BaseModel
from app.extensions import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Relations
    places = db.relationship('Place', backref='owner', cascade="all, delete-orphan", lazy=True)
    reviews = db.relationship('Review', backref='user', cascade="all, delete-orphan", lazy=True)

    @property
    def password(self):
        """Prevent reading password directly"""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password_text):
        """Generate a hashed password"""
        if not password_text:
            raise ValueError("Password cannot be empty")
        self.password_hash = bcrypt.generate_password_hash(password_text).decode('utf-8')

    def verify_password(self, password_text):
        """Verify the password hash"""
        if not self.password_hash:
            return False
        return bcrypt.check_password_hash(self.password_hash, password_text)

    def to_dict(self):
        """Complete serialization of User (excludes password)"""
        data = super().to_dict()
        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })
        return data

    def to_nested_dict(self):
        """Simplified serialization for nested objects (in reviews, places)"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

    def __repr__(self):
        return f"<User {self.email}>"