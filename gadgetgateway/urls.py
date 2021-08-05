from django.urls import path, include
from gadgetgateway import views
from allauth.account.views import LoginView, SignupView 

app_name = 'gadgetgateway'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('news/', views.news, name='news'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('category/<slug:category_name_slug>/<slug:product_name_slug>/like', views.like_product, name='like_product'),
    path('category/<slug:category_name_slug>/<slug:product_name_slug>', views.view_product, name='view_product'),
    path('category/<slug:category_name_slug>/add_product/', views.add_product, name="add_product"),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('restricted/', views.restricted, name="restricted"),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.search, name='search'),

    # path('account/login/', LoginView.as_view(), name="login" ),
    # path('account/signup/', SignupView.as_view(), name="register" ),
]
