from django.urls import path
from gadgetgateway import views

app_name = 'gadgetgateway'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('news/', views.news, name='news'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('restricted/', views.restricted, name="restricted"),
    path('logout/', views.user_logout, name='logout'),
    path('<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('<slug:category_name_slug>/<slug:product_name_slug>/like', views.like_product, name='like_product'),
    path('<slug:category_name_slug>/<slug:product_name_slug>/dislike', views.dislike_product, name='dislike_product'),
    path('<slug:category_name_slug>/<slug:product_name_slug>/undo_reactions', views.undo_reactions, name='undo_reactions'),
    path('<slug:category_name_slug>/<slug:product_name_slug>', views.view_product, name='view_product'),
    path('<slug:category_name_slug>/add_product/', views.add_product, name="add_product"),
]
