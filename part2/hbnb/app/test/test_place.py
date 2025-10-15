import unittest
from datetime import datetime
from app.models.place import Place
from app.models.user import User

class TestPlace(unittest.TestCase):

    def setUp(self):
        self.now_str = datetime.now().isoformat()
        
        self.owner = User(
            id='owner-123', 
            first_name='Owner', 
            last_name='Test', 
            email='owner@test.com',
            is_admin=False,
            created_at=self.now_str, 
            updated_at=self.now_str
        )
        
        self.valid_place_data = {
            'id': 'place-456',
            'title': 'Appartement de luxe',
            'description': 'Description du lieu',
            'price': 150,
            'latitude': 45.75,
            'longitude': 4.83,
            'owner': self.owner,
            'created_at': self.now_str,
            'updated_at': self.now_str
        }
        self.place = Place(**self.valid_place_data)

    def test_place_creation_and_attributes(self):
        self.assertIsInstance(self.place, Place)
        self.assertEqual(self.place.title, 'Appartement de luxe')
        self.assertEqual(self.place.owner.id, 'owner-123')
        self.assertTrue(self.place.validate)

    def test_place_validation_price_negative(self):
        self.place.price = -10
        with self.assertRaises(ValueError) as context:
            self.place.validate
        self.assertIn("price must be positive", str(context.exception))
        
    def test_place_validation_title_empty(self):
        self.place.title = ''
        with self.assertRaises(ValueError) as context:
            self.place.validate
        self.assertIn("title cannot be empty", str(context.exception))

    def test_place_validation_invalid_latitude(self):
        self.place.latitude = 95.0
        with self.assertRaises(ValueError) as context:
            self.place.validate
        self.assertIn("latitude must be between -90 and 90", str(context.exception))

    def test_place_validation_invalid_longitude(self):
        self.place.longitude = 190.0
        with self.assertRaises(ValueError) as context:
            self.place.validate
        self.assertIn("longitude must be between -180 and 180", str(context.exception))

if __name__ == '__main__':
    unittest.main()