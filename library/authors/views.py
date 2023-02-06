from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from .models import Author, Biography, Book, Article
from .serializers import AuthorModelSerializer, AuthorModelSerializer2, BiographyModelSerializer, BookModelSerializer, ArticleModelSerializer
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination


class AuthorPaginator(LimitOffsetPagination):
    default_limit = 10


class AuthorModelViewSet(ModelViewSet):
    queryset = Author.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = AuthorModelSerializer
    # filterset_fields = ['first_name', 'last_name', 'birthday_year']
    # pagination_class = AuthorPaginator


class BiographyModelViewSet(ModelViewSet):
    queryset = Biography.objects.all()
    serializer_class = BiographyModelSerializer


class BookModelViewSet(ModelViewSet):
    # permission_classes = [AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer


class ArticleModelViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer


class MyAPIView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer = AuthorModelSerializer

    def get_serializer_class(self):
        if self.request.version == '1':
            return AuthorModelSerializer
        return AuthorModelSerializer2


