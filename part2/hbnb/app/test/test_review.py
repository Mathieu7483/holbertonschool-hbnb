# tests/test_models/test_review.py

import unittest
from app.models.review import Review
from datetime import datetime

class TestReview(unittest.TestCase):
    """Tests unitaires pour la classe Review."""

    def setUp(self):
        self.now = datetime.now()
        self.valid_review_data = {
            'id': 'review-101',
            'name': 'Excellente expérience',
            'text': 'C\'était vraiment super !',
            'place_id': 'place-202',
            'user_id': 'user-303',
            'created_at': self.now,
            'updated_at': self.now
        }
        self.review = Review(**self.valid_review_data)

    def test_review_creation_and_attributes(self):
        """Vérifie la création et les attributs de l'objet Review."""
        self.assertIsInstance(self.review, Review)
        self.assertEqual(self.review.name, 'Excellente expérience')
        self.assertEqual(self.review.text, 'C\'était vraiment super !')
        self.assertEqual(self.review.place_id, 'place-202')
        self.assertEqual(self.review.user_id, 'user-303')
        self.assertEqual(self.review.created_at, self.now)
        self.assertEqual(self.review.updated_at, self.now)
        self.assertEqual(self.review.id, 'review-101')
        self.assertTrue(hasattr(self.review, 'to_dict'))
        self.assertTrue(callable(getattr(self.review, 'to_dict', None)))
        self.assertTrue(hasattr(self.review, 'update'))
        self.assertTrue(callable(getattr(self.review, 'update', None)))
        self.assertTrue(hasattr(self.review, 'validate'))
        self.assertTrue(callable(getattr(self.review, 'validate', None)))
        self.assertTrue(hasattr(self.review, 'save'))
        self.assertTrue(callable(getattr(self.review, 'save', None)))
        self.assertTrue(hasattr(self.review, 'delete'))
        self.assertTrue(callable(getattr(self.review, 'delete', None))) 
        self.assertTrue(hasattr(self.review, 'reload'))
        self.assertTrue(callable(getattr(self.review, 'reload', None)))
        self.assertTrue(hasattr(self.review, 'to_json'))
        self.assertTrue(callable(getattr(self.review, 'to_json', None)))
        self.assertTrue(hasattr(self.review, 'from_json'))
        self.assertTrue(callable(getattr(self.review, 'from_json', None)))
        self.assertTrue(hasattr(self.review, 'from_dict'))
        self.assertTrue(callable(getattr(self.review, 'from_dict', None)))
        self.assertTrue(hasattr(self.review, 'to_str'))
        self.assertTrue(callable(getattr(self.review, 'to_str', None)))
        self.assertTrue(hasattr(self.review, 'to_repr'))
        self.assertTrue(callable(getattr(self.review, 'to_repr', None)))
        self.assertTrue(hasattr(self.review, 'clone'))
        self.assertTrue(callable(getattr(self.review, 'clone', None)))
        self.assertTrue(hasattr(self.review, 'compare'))
        self.assertTrue(callable(getattr(self.review, 'compare', None)))
        self.assertTrue(hasattr(self.review, 'is_valid'))
        self.assertTrue(callable(getattr(self.review, 'is_valid', None)))
        self.assertTrue(hasattr(self.review, 'full_validate'))
        self.assertTrue(callable(getattr(self.review, 'full_validate', None)))
        self.assertTrue(hasattr(self.review, 'partial_validate'))
        self.assertTrue(callable(getattr(self.review, 'partial_validate', None)))
        self.assertTrue(hasattr(self.review, 'clear'))
        self.assertTrue(callable(getattr(self.review, 'clear', None)))
        self.assertTrue(hasattr(self.review, 'reset'))
        self.assertTrue(callable(getattr(self.review, 'reset', None)))
        self.assertTrue(hasattr(self.review, 'is_empty'))
        self.assertTrue(callable(getattr(self.review, 'is_empty', None)))
        self.assertTrue(hasattr(self.review, 'is_equal'))
        self.assertTrue(callable(getattr(self.review, 'is_equal', None)))
        self.assertTrue(hasattr(self.review, 'is_different'))
        self.assertTrue(callable(getattr(self.review, 'is_different', None)))
        self.assertTrue(hasattr(self.review, 'get_changes'))
        self.assertTrue(callable(getattr(self.review, 'get_changes', None)))
        self.assertTrue(hasattr(self.review, 'set_attributes'))
        self.assertTrue(callable(getattr(self.review, 'set_attributes', None)))
        self.assertTrue(hasattr(self.review, 'get_attributes'))
        self.assertTrue(callable(getattr(self.review, 'get_attributes', None)))
if __name__ == '__main':
    unittest.main()