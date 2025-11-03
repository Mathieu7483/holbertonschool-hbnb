from app.extensions import db, bcrypt
from app.models.basemodel import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False) # Renommé pour plus de clarté
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # --- RELATIONS ---
    places = db.relationship('Place', backref='owner', cascade="all, delete-orphan", lazy=True)
    reviews = db.relationship('Review', backref='user', cascade="all, delete-orphan", lazy=True)
    
    # --- SUPPRESSION DE __init__, validate, update_from_dict ---

    @property
    def password(self):
        raise AttributeError('Le mot de passe ne peut pas être lu.')

    @password.setter
    def password(self, password_text):
        """Génère un hash à partir du mot de passe et le stocke."""
        self.password_hash = bcrypt.generate_password_hash(password_text).decode('utf-8')

    def verify_password(self, password_text):
        """Vérifie si le mot de passe fourni correspond au hash."""
        return bcrypt.check_password_hash(self.password_hash, password_text)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })
        return data