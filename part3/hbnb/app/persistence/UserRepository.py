from app.models.user import User
from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
    def delete(self, obj_id):
        """Delete a user by ID"""
        user = self.get(obj_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False