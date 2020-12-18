import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def post_image_file_path(instance, filename):
    """generate a file path for new post image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('upload/post', filename)

class Category(models.Model):
    """This is table for Category"""
    categoryName = models.CharField(max_length=255)

    def __str__(self):
        return self.categoryName


class Post(models.Model):
    """This is model for post"""
    categoryName = models.ForeignKey(Category,related_name="posts", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(null=True, upload_to=post_image_file_path)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

