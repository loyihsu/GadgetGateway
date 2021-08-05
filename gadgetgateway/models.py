from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from tango_with_django_project import settings
from django.urls import reverse

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_image', blank=True)

    slug = models.SlugField(unique=True)

    views = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def number_of_likes(self):
        return self.votes.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, ** kwargs)

    def __str__(self):
        return self.name

    # Get the article address
    def get_absolute_url(self):
        return reverse('gadgetgateway:product', args=[self.name, self.category])

class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, default=1, on_delete=CASCADE)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.comment, self.user)

class UserProfile(models.Model):
    # Link to map UserProfile to a user model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional attributes to be included
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
