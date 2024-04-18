# models.py

from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
from django.contrib.auth.models import BaseUserManager
from djongo import models as djmodels
from djongo.models.fields import ArrayReferenceField
from djongo.storage import GridFSStorage

grid_fs_storage = GridFSStorage(collection='pdf')

class Document(models.Model):
    _id = djmodels.ObjectIdField()
    #id = models.BigAutoField( primary_key=True, editable=False, db_column='_id')
    file= djmodels.FileField(upload_to='pdf/')
    filename = djmodels.CharField(max_length=255)
    content_type = djmodels.CharField(max_length=100)
    size = djmodels.IntegerField()
    uploaded_at = djmodels.DateTimeField(auto_now_add=True)
    def __getattribute__(self, attr):
        return super().__getattribute__(attr)
    def __id__(self):
        return self._id
    def __str__(self):
        return self.filename
    def save(self, *args, **kwargs):
        self.id = self._id
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



###This is just an example, has to be modified
class InputOutput(models.Model): 
    # Define fields for the InputOutput model
    # For example, you might have fields like 'message', 'timestamp', etc.
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Index(models.Model):
    index_value = models.IntegerField()

    def __str__(self):
        return str(self.index_value)

class ChatHistory(models.Model):
    _id = djmodels.ObjectIdField()
    user_id = models.IntegerField()
    inputoutput = models.ManyToManyField(to=InputOutput)
    pinned_indices = models.ManyToManyField(to=Index, blank=True)
    embedding_id = models.IntegerField()

