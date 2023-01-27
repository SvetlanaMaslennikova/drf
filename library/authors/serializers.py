from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from .models import Author, Biography, Book, Article


class AuthorModelSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        # exclude = ['id']


class BiographyModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Biography
        fields = '__all__'


class BookModelSerializer(ModelSerializer):
    # authors = AuthorModelSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'


class ArticleModelSerializer(HyperlinkedModelSerializer):
    author = AuthorModelSerializer()

    class Meta:
        model = Article
        fields = '__all__'
