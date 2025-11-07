from app.models.review import Review
from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository
from typing import Optional, Any

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)
        
    def get(self, entity_id: str) -> Optional[Review]:
        """
        Retrieves a Review entity by its string ID.
        This method is defined here to ensure the correct filter method is used,
        overriding a potentially flawed generic 'get' from the parent repository.
        """
        # We ensure that the string ID is passed to the filter, which resolves the ProgrammingError.
        return self.model.query.filter_by(id=entity_id).first()

    def delete(self, obj_or_id: Any) -> bool:
        """
        Deletes a review entity. This method overrides the generic delete 
        to correctly handle both object instances (passed from Façade) or string IDs.
        """
        obj_to_delete = None

        if isinstance(obj_or_id, self.model):
            # Case 1: An object instance is passed (common from Facade)
            obj_to_delete = obj_or_id
        else:
            # Case 2: Assume an ID string is passed
            obj_to_delete = self.get(obj_or_id)

        if not obj_to_delete:
            return False

        try:
            # Perform the deletion and commit the transaction
            db.session.delete(obj_to_delete)
            db.session.commit()
            return True
        except Exception:
            # Rollback on any error to ensure session integrity
            db.session.rollback()
            return False

    def get_by_attributes(self, **kwargs: Any) -> Optional[Review]:
        """
        Retrieves a single review based on multiple attribute filters (e.g., user_id and place_id).
        """
        return db.session.execute(
            db.select(self.model).filter_by(**kwargs)
        ).scalar_one_or_none()