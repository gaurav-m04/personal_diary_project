from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    """serialize the user modal"""
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        """Meta class"""
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        data = validated_data
        email, password = data['email'], data['password']
        del data['email'], data['password']
        return models.User.objects.create_user(email, password, **data)


class ComposeSerializer(serializers.ModelSerializer):
    """serialize the compose modal"""

    class Meta:
        model = models.Compose
        fields = ['id', 'title', 'image', 'description', 'composer', 'compose_date']


class ContactSerializer(serializers.ModelSerializer):
    """serialize the contact modal"""

    class Meta:
        model = models.Contact
        fields = '__all__'
