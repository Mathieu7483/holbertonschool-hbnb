import unittest
from unittest.mock import MagicMock, patch
from app.services.facade import HBnBFacade
from app.models.user import User

class TestUserFacade(unittest.TestCase):
    
    @patch('app.services.facade.InMemoryRepository') 
    def setUp(self, MockRepository):
        self.facade = HBnBFacade()
        self.mock_repo = self.facade.user_repo

    @patch('app.services.facade.uuid4', return_value='new-uuid-1234')
    def test_create_user_success(self, mock_uuid):
        user_data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com'
        }
        
        new_user = self.facade.create_user(user_data)

        self.assertIsInstance(new_user, User)
        self.assertEqual(new_user.id, 'new-uuid-1234')
        self.mock_repo.add.assert_called_once_with(new_user)
        self.assertEqual(new_user.first_name, 'Alice')

    def test_get_user(self):
        mock_user = MagicMock(spec=User)
        self.mock_repo.get.return_value = mock_user

        user_retrieved = self.facade.get_user('user-id-a')

        self.mock_repo.get.assert_called_once_with('user-id-a')
        self.assertEqual(user_retrieved, mock_user)

    def test_get_all_users(self):
        self.mock_repo.get_all.return_value = [MagicMock(spec=User), MagicMock(spec=User)]

        users = self.facade.get_all_users()

        self.mock_repo.get_all.assert_called_once()
        self.assertEqual(len(users), 2)
        
if __name__ == '__main__':
    unittest.main()