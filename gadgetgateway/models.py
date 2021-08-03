from django.db import models
from django.db.models.fields.related import ForeignKey
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

# Category of the products
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, ** kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=240)
    # Assuming each product can have only one category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    slug = models.SlugField(unique=True)

    views = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, ** kwargs)

    def __str__(self):
        return self.name

class Comment(models.Model):
    product = ForeignKey(Product, on_delete=models.CASCADE)
    text = models.CharField(max_length=5000)
    date = models.DateField()
    recommended = models.BooleanField()
    # May need to include user as foreign key if we want to show users

    def __str__(self):
        return self.text

class UserProfile(models.Model):
    # Link to map UserProfile to a user model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional attributes to be included
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
