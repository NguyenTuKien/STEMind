from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


class Category(models.Model):
    category_name = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name
    
class File(models.Model):
    title = models.TextField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Files')
    file_thumbnail = models.ImageField(upload_to='thumbnails/%y/%m/%d', blank=True, null=True, default='default.jpg')
    file_description = models.TextField(blank=True, null=True)
    file_urls = models.FileField(upload_to='uploads/%y/%m/%d')
    file_status = models.IntegerField(choices=[(0, 'Draft'), (1, 'Published')], default=0)
    file_views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "File"
        verbose_name_plural = "Files"


 