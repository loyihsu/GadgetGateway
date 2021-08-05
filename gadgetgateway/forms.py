from django import forms
from django.forms import fields
from django.contrib.auth.models import User

from gadgetgateway.models import Category, Product, UserProfile, Comment

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)


class ProductForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the name of the product.")
    description = forms.CharField(max_length=100, help_text="A quick description of the product. (100 characters)")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    image = forms.ImageField()
    
    class Meta:
        model = Product
        exclude = ('category',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class CommentForm(forms.ModelForm):
    recommended = forms.BooleanField(help_text="Do you recommend this product?", required=False)
    class Meta:
        model = Comment
        fields = ('comment', 'recommended')

