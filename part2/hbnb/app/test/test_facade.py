import unittest
from unittest.mock import MagicMock, patch
from app.services.facade import HBnBFacade # Votre classe Facade
from app.models.user import User # Votre modèle User

class TestUserFacade(unittest.TestCase):
    """Tests unitaires pour les méthodes User dans le Facade."""

    @patch('app.persistence.repository.InMemoryRepository')
    def setUp(self, MockRepository):
        """Configure le Facade avec un dépôt simulé (Mocked Repository)."""
        self.mock_repo = MockRepository.return_value 
        
        self.facade = HBnBFacade()

    @patch('app.services.facade.uuid4', return_value='new-uuid-1234')
    def test_create_user_success(self, mock_uuid):
        """Vérifie la création d'un utilisateur et l'appel au dépôt."""
        user_data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com'
        }
        
        new_user = self.facade.create_user(user_data)

        # 1. Vérifie que l'objet créé est bien un User
        self.assertIsInstance(new_user, User)
        # 2. Vérifie que la logique d'ID a été appliquée
        self.assertEqual(new_user.id, 'new-uuid-1234')
        # 3. Vérifie que le dépôt a été appelé pour enregistrer l'utilisateur
        self.mock_repo.add.assert_called_once_with(new_user)
        # 4. Vérifie que l'objet est retourné
        self.assertEqual(new_user.first_name, 'Alice')

    def test_get_user(self):
        """Vérifie la récupération d'un utilisateur par ID."""
        # Configure le dépôt simulé pour retourner un objet factice
        mock_user = MagicMock(spec=User)
        self.mock_repo.get.return_value = mock_user

        user_retrieved = self.facade.get_user('user-id-a')

        # 1. Vérifie que le dépôt a été appelé avec le bon ID
        self.mock_repo.get.assert_called_once_with('user-id-a')
        # 2. Vérifie que l'utilisateur est bien celui retourné par le mock
        self.assertEqual(user_retrieved, mock_user)

    def test_get_all_users(self):
        """Vérifie la récupération de tous les utilisateurs."""
        # Configure le dépôt simulé pour retourner une liste d'objets factices
        self.mock_repo.get_all.return_value = [MagicMock(spec=User), MagicMock(spec=User)]

        users = self.facade.get_all_users()

        self.mock_repo.get_all.assert_called_once()
        self.assertEqual(len(users), 2)
        
if __name__ == '__main__':
    unittest.main()