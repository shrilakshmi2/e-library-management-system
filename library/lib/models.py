from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
import re
import logging
from django.contrib import messages
from django.core.exceptions import ValidationError



class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    student_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    book1 = models.ForeignKey(
        'Book', related_name='book1', on_delete=models.SET_NULL, null=True, blank=True)
    book2 = models.ForeignKey(
        'Book', related_name='book2', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    book_id = models.IntegerField(unique=True)
    isbn_number = models.CharField(max_length=13, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
   



class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.admin_id}"
    
    

    
    
