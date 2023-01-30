import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APISimpleTestCase, APITestCase
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from .views import AuthorModelViewSet, BookModelViewSet
from .models import Author, Book


class TestAuthorViewSet(TestCase):

    def test_get_list(self):
        factory = APIRequestFactory()
        request = factory.get('/api/authors')
        view = AuthorModelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_quest(self):
        factory = APIRequestFactory()
        request = factory.post('/api/authors', {
            'first_name': 'Александр',
            'last_name': 'Пушкин',
            'birthday_year': 1799
        })
        view = AuthorModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_admin(self):
        factory = APIRequestFactory()
        request = factory.post('/api/authors', {
            'first_name': 'Александр',
            'last_name': 'Пушкин',
            'birthday_year': 1799
        })
        admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        force_authenticate(request, admin)
        view = AuthorModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_detail(self):
        author = Author.objects.create(first_name='Александр', last_name='Пушкин', birthday_year=1799)
        client = APIClient()
        response = client.get(f'/api/authors/{author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_guest(self):
        author = Author.objects.create(first_name='Александр', last_name='Пушкин', birthday_year=1799)
        client = APIClient()
        response = client.put(f'/api/authors/{author.id}/', {'first_name': 'Говард', 'last_name': 'Лавкрафт', 'birthday_year': 1880})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_admin(self):
        author = Author.objects.create(first_name='Александр', last_name='Пушкин', birthday_year=1799)
        client = APIClient()
        admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        client.login(username='admin', password='admin')
        response = client.put(f'/api/authors/{author.id}/',
                              {'first_name': 'Говард', 'last_name': 'Лавкрафт', 'birthday_year': 1880})
        author = Author.objects.get(pk=author.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(author.first_name, 'Говард')
        self.assertEqual(author.last_name, 'Лавкрафт')
        self.assertEqual(author.birthday_year, 1880)
        client.logout()


class TestMath(APISimpleTestCase):
    def test_sqrt(self):
        import math
        self.assertEqual(math.sqrt(4), 2)


class TestBoolViewSet(APITestCase):

    def test_get_lists(self):
        response = self.client.get('/api/book/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_book_admin(self):
        # author = Author.objects.create(first_name='Александр', last_name='Пушкин', birthday_year=1799)
        # book = Book.objects.create(name='Руслан и Людмила')
        # book.authors.add(author)
        # book.save()

        book = mixer.blend(Book)

        admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        self.client.login(username='admin', password='admin')
        response = self.client.put(f'/api/book/{book.id}/',
                                   {'name': 'Пиковая дама', 'author': book.authors})

        book = Book.objects.get(id=book.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(book.name, 'Пиковая дама')
        self.client.logout()
