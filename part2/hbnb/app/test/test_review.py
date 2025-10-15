import unittest
from datetime import datetime
from app.models.review import Review
from app.models.place import Place
from app.models.user import User

class TestReview(unittest.TestCase):

    def setUp(self):
        self.now_str = datetime.now().isoformat()
        
        self.mock_user = User(
            id='user-303', first_name='Test', last_name='User', 
            email='u@test.com', is_admin=False, created_at=self.now_str, updated_at=self.now_str
        )
        self.mock_place = Place(
            id='place-202', title='Lieu Test', description='Test desc', price=100, owner=self.mock_user,
            latitude=0.0, longitude=0.0, created_at=self.now_str, updated_at=self.now_str
        )
        
        self.valid_review_data = {
            'id': 'review-101',
            'text': 'C\'était vraiment super !',
            'created_at': self.now_str,
            'updated_at': self.now_str
        }
        
        self.review = Review(
            rating=5,
            place=self.mock_place,
            user=self.mock_user,
            **self.valid_review_data
        )

    def test_review_creation_and_attributes(self):
        self.assertIsInstance(self.review, Review)
        self.assertEqual(self.review.text, 'C\'était vraiment super !')
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.place.id, 'place-202')
        self.assertEqual(self.review.user.id, 'user-303')
        self.assertEqual(self.review.created_at, self.now_str)
        self.assertEqual(self.review.updated_at, self.now_str)
        self.assertEqual(self.review.id, 'review-101')
        self.assertTrue(self.review.validate)

    def test_review_validation_text_empty(self):
        self.review.text = ''
        with self.assertRaises(ValueError) as context:
            self.review.validate
        self.assertIn("text cannot be empty", str(context.exception))

    def test_review_validation_missing_place_id(self):
        self.review.rating = 0
        with self.assertRaises(ValueError) as context:
            self.review.validate
        self.assertIn("rating must be between 1 and 5", str(context.exception))
        
    def test_review_validation_missing_user_id(self):
        self.review.rating = 6
        with self.assertRaises(ValueError) as context:
            self.review.validate
        self.assertIn("rating must be between 1 and 5", str(context.exception))

if __name__ == '__main__':
    unittest.main()