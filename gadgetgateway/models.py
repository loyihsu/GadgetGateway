from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField
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

    def get_likes(self):
        votes = Vote.objects.all().filter(votee=self, positivity=True)
        return len(votes)

    def get_satisfactory_rate(self):
        votes = Vote.objects.all().filter(votee=self)
        positive = votes.filter(positivity=True)
        negative = votes.filter(positivity=False)
        if len(votes) == 0:
            return 0
        return len(positive) - len(negative)

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
    comment = models.TextField(blank=True)
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

class Vote(models.Model):
    voter = ForeignKey(User, on_delete=CASCADE)
    votee = ForeignKey(Product, on_delete=CASCADE)
    positivity = BooleanField()

class News(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title
