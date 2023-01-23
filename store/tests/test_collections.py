from django.contrib.auth.models import User
from store.models import Collection
from rest_framework.test import APIClient
from rest_framework import status
import pytest
from model_bakery import baker

# @pytest.fixture
# def create_collection(api_client):
#     api_client.post('/store/collections/')

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_user_is_not_admin_returns_403(self, api_client, create_collection, authenticate):
        authenticate(is_staff=False)
        
        response = create_collection({'title': 'a'})

        #Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    
    def test_if_data_is_invalid_returns_400(self):
        #Arrange

        #Act
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {'title': ' '})

        #Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None


    def test_if_data_is_valid_returns_201(self):
        #Arrange

        #Act
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {'title': 'a'})

        #Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
    
@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        #Arrange
        #Collection.objects.create(title='a')
        collection = baker.make(Collection)
        
        response = api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }

    
    def test_if_collection_dosent_exist_return_404(self, api_client):
        collection = Collection.objects.all()

        response = api_client.get(f'/store/collections/{collection}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND