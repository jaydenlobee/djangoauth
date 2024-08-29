from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    phone_number = models.CharField('phone number', max_length=15, unique=True, blank=True, null=True)
    address = models.CharField('address', max_length=100, blank=True, null=True)
    city = models.CharField('city', max_length=50, blank=True, null=True)
    country = models.CharField('country', max_length=50, blank=True, null=True)
    postal_code = models.CharField('zip/postal code', max_length=10, blank=True, null=True)
    profile_picture = models.ImageField('profile picture', upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField('date of birth', blank=True, null=True)
    gender = models.CharField('gender', max_length=10, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
