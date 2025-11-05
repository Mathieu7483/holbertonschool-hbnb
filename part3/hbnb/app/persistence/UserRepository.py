from app.models.user import User
from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
    def delete(self, obj):
        """Deletes a given object from the database."""
        if not obj:
            return False 
        try:
            db.session.delete(obj)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting object: {e}")
            return False