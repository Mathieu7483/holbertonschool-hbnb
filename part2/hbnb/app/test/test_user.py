# tests/test_models/test_user.py

import unittest
from datetime import datetime
from app.models.user import User
from app.models.basemodel import BaseModel # Assurez-vous d'importer la bonne BaseModel

class TestUser(unittest.TestCase):
    """Tests unitaires pour la classe User."""

    def setUp(self):
        """Initialise un objet User de base pour les tests."""
        self.now = datetime.now()
        # Note : On suppose que l'ID est généré ailleurs (dans le Facade par exemple)
        self.valid_user_data = {
            'id': 'test-1234',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean.dupont@test.fr',
            'is_admin': False,
            'created_at': self.now,
            'updated_at': self.now
        }
        self.user = User(**self.valid_user_data)

    def test_user_creation_and_attributes(self):
        """Vérifie la création et l'héritage des attributs."""
        self.assertIsInstance(self.user, User)
        self.assertIsInstance(self.user, BaseModel)
        self.assertEqual(self.user.email, 'jean.dupont@test.fr')

    def test_user_validation_valid(self):
        """Vérifie que la validation passe avec des données valides."""
        # La validation est déclenchée par l'accès à la propriété
        self.assertTrue(self.user.validate)

    def test_user_validation_invalid_email(self):
        """Vérifie l'échec de la validation pour un email invalide."""
        self.user.email = 'email-invalide'
        with self.assertRaises(ValueError) as context:
            self.user.validate
        self.assertIn("email must be a valid email address", str(context.exception))

    def test_user_validation_empty_first_name(self):
        """Vérifie l'échec de la validation pour un prénom vide."""
        self.user.first_name = ''
        with self.assertRaises(ValueError) as context:
            self.user.validate
        self.assertIn("first_name cannot be empty", str(context.exception))

    def test_user_update_attributes(self):
        """Vérifie que la méthode update met à jour les attributs."""
        new_data = {'first_name': 'Pierre', 'last_name': 'Durand'}
        
        # NOTE IMPORTANTE : Retirez l'appel self.save() de la méthode update()
        # si ce n'est pas déjà fait, pour que ce test reste unitaire.
        
        self.user.update(new_data) 
        self.assertEqual(self.user.first_name, 'Pierre')
        self.assertEqual(self.user.last_name, 'Durand')

if __name__ == '__main__':
    unittest.main()