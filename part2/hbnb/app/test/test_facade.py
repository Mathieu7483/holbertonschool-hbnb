import unittest
from unittest.mock import MagicMock, patch
from app.services.facade import HBnBFacade
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from datetime import datetime

class BaseFacadeTest(unittest.TestCase):

    @patch('app.services.facade.InMemoryRepository') 
    def setUp(self, MockRepository):
        self.facade = HBnBFacade()
        
        self.user_repo_mock = self.facade.user_repo
        self.place_repo_mock = self.facade.place_repo
        self.review_repo_mock = self.facade.review_repo
        self.amenity_repo_mock = self.facade.amenity_repo

class TestUserFacade(BaseFacadeTest):
    
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
        self.user_repo_mock.add.assert_called_once_with(new_user)
        self.assertEqual(new_user.first_name, 'Alice')

    def test_get_user(self):
        mock_user = MagicMock(spec=User)
        self.user_repo_mock.get.return_value = mock_user

        user_retrieved = self.facade.get_user('user-id-a')

        self.user_repo_mock.get.assert_called_once_with('user-id-a')
        self.assertEqual(user_retrieved, mock_user)

class TestPlaceFacade(BaseFacadeTest):
    
    @patch('app.services.facade.uuid4', return_value='new-place-id-456')
    @patch('app.services.facade.User') 
    def test_create_place_success(self, MockedUserClassInFacade, mock_uuid):
        now_str = datetime.now().isoformat()
        owner_id = 'owner-id-123'
        
        owner_instance = User(
            id=owner_id, first_name='Test', last_name='Owner', 
            email='test@owner.com', is_admin=False, created_at=now_str, updated_at=now_str
        )
        
        owner_instance.to_dict = MagicMock(return_value={
            'id': owner_id, 
            'first_name': 'Test', 
            'last_name': 'Owner'
        })

        self.user_repo_mock.get.return_value = owner_instance
        
        place_data = {
            'title': 'Chalet en montagne',
            'description': 'Superbe vue',
            'price': 200,
            'owner_id': owner_id,
            'latitude': 45.0,
            'longitude': 6.0
        }
        
        new_place_dict = self.facade.create_place(place_data) 
        
        self.user_repo_mock.get.assert_called_once_with(owner_id)
        self.place_repo_mock.add.assert_called_once()
        self.assertEqual(new_place_dict['id'], 'new-place-id-456')
        self.assertEqual(new_place_dict['owner']['id'], owner_id)

    def test_get_place(self):
        mock_owner_with_dict = MagicMock(spec=User, id='owner-id-mocked')
        mock_owner_with_dict.to_dict.return_value = {
            'id': 'owner-id-mocked', 
            'email': 'mock@test.com',
            'created_at': 'mock_date',
            'updated_at': 'mock_date'
        }

        mock_place = MagicMock(
            spec=Place, 
            id='place-id-a-mocked', 
            title='Lieu Mocké',
            description='Test desc',
            price=100,
            latitude=45.0,
            longitude=6.0,
            owner=mock_owner_with_dict,
            amenities=[], 
            created_at='mock_date',
            updated_at='mock_date'
        )
        self.place_repo_mock.get.return_value = mock_place

        place_retrieved_dict = self.facade.get_place('place-id-a')

        self.place_repo_mock.get.assert_called_once_with('place-id-a')
        self.assertEqual(place_retrieved_dict['id'], 'place-id-a-mocked')
        self.assertEqual(place_retrieved_dict['owner']['id'], 'owner-id-mocked')

class TestReviewFacade(BaseFacadeTest):
    
    @patch('app.services.facade.uuid4', return_value='new-review-id-789')
    def test_create_review_success(self, mock_uuid):
        mock_user = MagicMock(spec=User, id='user-id-303')
        mock_place = MagicMock(spec=Place, id='place-id-202')
        
        review_data = {
            'text': 'Très bonne note',
            'rating': 5,
            'place': mock_place,
            'user': mock_user
        }
        
        new_review = self.facade.create_review(review_data)

        self.assertIsInstance(new_review, Review)
        self.assertEqual(new_review.id, 'new-review-id-789')
        self.review_repo_mock.add.assert_called_once_with(new_review)

    def test_get_review(self):
        mock_review = MagicMock(spec=Review, id='review-id-b-mocked')
        self.review_repo_mock.get.return_value = mock_review

        review_retrieved = self.facade.get_review('review-id-b')

        self.review_repo_mock.get.assert_called_once_with('review-id-b')
        self.assertEqual(review_retrieved, mock_review)

class TestAmenityFacade(BaseFacadeTest):
    
    @patch('app.services.facade.uuid4', return_value='new-amenity-id-101')
    def test_create_amenity_success(self, mock_uuid):
        amenity_data = {
            'name': 'Piscine'
        }
        
        new_amenity = self.facade.create_amenity(amenity_data)

        self.assertIsInstance(new_amenity, Amenity)
        self.assertEqual(new_amenity.id, 'new-amenity-id-101')
        self.amenity_repo_mock.add.assert_called_once_with(new_amenity)
        self.assertEqual(new_amenity.name, 'Piscine')

    def test_get_amenity(self):
        mock_amenity = MagicMock(spec=Amenity, id='amenity-id-c-mocked')
        self.amenity_repo_mock.get.return_value = mock_amenity

        amenity_retrieved = self.facade.get_amenity('amenity-id-c')

        self.amenity_repo_mock.get.assert_called_once_with('amenity-id-c')
        self.assertEqual(amenity_retrieved, mock_amenity)

if __name__ == '__main__':
    unittest.main()