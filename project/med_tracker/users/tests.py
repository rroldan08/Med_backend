from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from factory import DjangoModelFactory, Faker
from yaml import serialize
from models import User 
from serializers import *
from users import *
# Create your tests here.



class UserTestModel(DjangoModelFactory):
    name = Faker('roger')
    email = Faker('email.com')
    password = Faker('password123')

    class Meta:
        model = User

class UserTestCase(TestCase):
    def test_str(self):
        user = User()
        self.assertEqual(str(user), user.name)


class UserSerializer(TestCase):
    def test_model_fields(self):
        user = UserSerializer()

        for field_name in ['id', 'name', 'email', 'password']:
            self.assertEqual(serialize.data[field_name], getattr(user, field_name))




class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.user = UserTestModel(email='testuser@example.com')
        self.user.set_password('password123')
        self.user.save()
        self.client.login(email=self.user.email, password='password123')
        self.list_url = reverse('user-list')
    
    def get_details_url(self):
        return reverse(self.user, kwargs = {'id': id})

    
    def test_get_list(self):
        users = [User() for i in range(0, 3)]

        response = self.client.get(self.list_url)


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(user['id'] for user in response.data['results']), 
        set(user.id for user in users))
    

    def test_post(self):
        data = {
            'id': '1',
            'name': 'roger',
            'email': 'email.com',
            'password':  'password123'
        }
        self.assertEqual(User.object.count(), 0)
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.all().first()
        for field_name in data.keys():
            self.assertEqual(getattr(user, field_name), data[field_name])
    

    def test_put(self):
        user = User()

        data = {
            'id': '1',
            'name': 'roger',
            'email': 'email.com',
            'password':  'password123', 
        }

        response = self.client.put(
              self.get_detail_url(user.id),
              data=data
          )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        user.refresh_from_db()
        for field_name in data.keys():
            self.assertEqual(getattr(user, field_name), data[field_name])
        


    def test_patch(self):
          user = User()
          data = {'name': 'roger'}
          response = self.client.patch(
              self.get_detail_url(user.id),
              data=data
          )
          self.assertEqual(response.status_code, status.HTTP_200_OK)


          user.refresh_from_db()
          self.assertEqual(user.name, data['name'])
    

    def test_delete(self):
          user = User()
          response = self.client.delete(self.get_detail_url(user.id))
          self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)



class UserViewSetTestCase(TestCase):

      ...

      def test_unauthenticated(self):
          self.client.logout()
          user = User()

          with self.subTest('GET list page'):
              response = self.client.get(self.list_url)
              self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

          with self.subTest('GET detail page'):
              response = self.client.get(self.get_detail_url(user.id))
              self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

          with self.subTest('PUT'):
              data = {
                  'id': '1',
                  'name': 'roger',
                  'email': 'email.com',
                  'password': 'password123',
              }
              response = self.client.put(self.get_detail_url(user.id), data=data)
              self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
              user.refresh_from_db()
              self.assertNotEqual(user.name, data['name'])

          with self.subTest('PATCH'):
              data = {'name': 'roger'}
              response = self.client.patch(self.get_detail_url(user.id), data=data)
              self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
              user.refresh_from_db()
              self.assertNotEqual(user.name, data['name'])

          with self.subTest('POST'):
              data = {
                  'id': '1',
                  'name': 'roger2',
                  'email': 'email.com',
                  'password': 'password123',
              }
              response = self.client.put(self.list_url, data=data)
              self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

          with self.subTest('DELETE'):
              response = self.client.delete(self.get_detail_url(user.id))
              self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
              self.assertTrue(User.objects.filter(id=user.id).exists())
