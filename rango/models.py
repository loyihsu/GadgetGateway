#from re import T
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title