import io

from rest_framework import serializers


class Author:

    def __init__(self, name, year):
        self.name = name
        self.year = year


class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    year = serializers.IntegerField()

    def validate_year(self, value):
        if value < 0:
            raise serializers.ValidationError('Год рождения не должен быть отрицательным')
        return value

    def validate(self, attrs):
        if attrs['name'] == 'Alex' and attrs['year'] != 1799:
            raise serializers.ValidationError('Год рождения Пушкина Не верен!!!')
        return attrs

    def create(self, validated_data):
        return Author(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        return instance


data = {'name': 'Alex', 'year': 1799}
serializer = AuthorSerializer(data=data)
serializer.is_valid()
author = serializer.save()
print(author.name, author.year)

new = {'name': 'Babayka', 'year': 888}
serializer = AuthorSerializer(author, data=new, partial=True)
serializer.is_valid()
author1 = serializer.save()
print(author1.name, author1.year)
print(author1 is author)
