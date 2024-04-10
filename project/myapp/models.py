# models.py

from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
from django.contrib.auth.models import BaseUserManager
from djongo import models as djmodels
from djongo.models.fields import ArrayReferenceField

class Document(models.Model):
    #_id = djmodels.ObjectIdField()
    #id = models.BigAutoField( primary_key=True, editable=False, db_column='_id')
    file= djmodels.FileField(upload_to='pdf/')
    filename = djmodels.CharField(max_length=255)
    content_type = djmodels.CharField(max_length=100)
    size = djmodels.IntegerField()
    uploaded_at = djmodels.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
    def save(self, *args, **kwargs):
        self.id = 1
        super(Document, self).save(*args, **kwargs)
    
class File(models.Model):
    #id = models.BigAutoField( primary_key=True, editable=False, db_column='_id')
    #file_id = models.BigAutoField(unique=True) removes in order for migrate to work
    file=models.FileField(upload_to='pdf/')
    filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    size = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename

class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    #_id = djmodels.ObjectIdField()
    id = models.BigAutoField( primary_key=True, editable=False, db_column='id')
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    username = None
    documents = ArrayReferenceField(to=Document, on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
