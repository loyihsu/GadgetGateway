from django import forms
from django.forms import fields
from rango.models import Page, Category# , UserProfile
# from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.Name_MAX_LENGTH, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=Page.URL_MAX_LENGTH, help_text="Please enter url of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['ur'] = url

        return cleaned_data
    
    class Meta:
        model = Page
        exclude = ('category',)
        # or specify the fields to include
        # fields = ('title', 'url', 'views')


# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
# 
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('website', 'picture')