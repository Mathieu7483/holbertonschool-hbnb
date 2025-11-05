# app/models/user.py

from app.models.basemodel import BaseModel
from app.extensions import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Relations
    places = db.relationship('Place', backref='owner', cascade="all, delete-orphan", lazy=True)
    reviews = db.relationship('Review', backref='user', cascade="all, delete-orphan", lazy=True)



    @property
    def password(self):
        """Empêche la lecture directe du mot de passe."""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password_text):
        """
        Génère un hash à partir du mot de passe en clair et le stocke 
        dans la colonne 'password_hash'.
        """
        self.password_hash = bcrypt.generate_password_hash(password_text).decode('utf-8')

    def verify_password(self, password_text):
        """Vérifie si le mot de passe fourni correspond au hash stocké."""
        if not self.password_hash:
            return False
        return bcrypt.check_password_hash(self.password_hash, password_text)

    def to_dict(self):
        """Sérialise l'objet User."""
        data = super().to_dict()
        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })
        return data