"""Contains ORM model definitions for the app."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager
from phonenumber_field import modelfields


class User(AbstractUser):
    """Define a custom auth model with email as the username field."""
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} {self.id}"


class Compose(models.Model):
    """Store the details about stories"""
    title = models.CharField(max_length=150)
    description = models.TextField()
    composer = models.ForeignKey(User, related_name='composer', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default='')
    compose_date = models.DateField(auto_now=True, verbose_name='compose_date')

    def __str__(self):
        return f"{self.composer} {self.title}"


class Contact(models.Model):
    """Store the details about contacted persions"""
    email = models.EmailField()
    country = models.CharField(max_length=50)
    phone = modelfields.PhoneNumberField(null=False, blank=False)
    msg = models.TextField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.email} {self.country}"
