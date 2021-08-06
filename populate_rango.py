import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from gadgetgateway.models import Category, Product, News, Vote
from django.contrib.auth.models import User
from datetime import datetime
import random

def populate():
    laptop_products = [
        {'name': '13-inch M1 MacBook Pro',
         'description': 'The new MacBook Pro without a new design, featuring the first Apple Silicon chip.',
         'views': 2500},
        {'name': '2020 16-inch MacBook Pro',
         'description': 'The 16-inch MacBook Pro released in 2020. It is commonly mentioned as the last MacBook Pro with an Intel chip.',
         'views': 0},
         {'name': '16-inch M1 MacBook Pro',
         'description': 'The new MacBook Pro without a new design, featuring the first Apple Silicon chip.',
         'views': 0},
        {'name': '2020 16-inch MacBook Pro',
         'description': 'The 16-inch MacBook Pro released in 2020. It is commonly mentioned as the last MacBook Pro with an Intel chip.',
         'views': 0},
    ]

    smartphone_products = [
        {'name': 'iPhone 12 mini',
         'description': 'iPhone 12 mini is commonly named the smallest phone in 2020.',
         'views': 2000},
        {'name': 'iPhone 12 Pro Max',
         'description': 'iPhone 12 Pro Max is the best phone Apple have made so far.',
         'views': 50},
    ]

    wearable_products = [
        {'name': 'Apple Watch Series 6',
         'description': 'The Apple Watch Series 6 features a faster S6 chip and blood oxygen level tracking.',
         'views': 0},
        {'name': 'Huawei Watch 3 Pro',
         'description': 'Continuous Health Monitoring | Up to 14-Day Battery Life | Independent Calling',
         'views': 0},
    ]

    headphone_products = [
        {'name': 'Sony MDR-1AM2',
         'description': 'Affordable and approachable, the Sony MDR-1AM2 is a great starting pair of audiophile headphones',
         'views': 60},
        {'name': 'AirPods Pro',
         'description': 'AirPods Pro earphones featuring noise canceling technology, a new design, improved water resistance, and a $249 price tag',
         'views': 0},
    ]

    categories = {'Laptops': laptop_products, 'Smartphones': smartphone_products, 'Wearables': wearable_products, 'Headphones': headphone_products}

    test_users = create_test_users(number=100)

    for category, data in categories.items():
        cat = add_category(category)
        for product in data:
            add_product(product['name'], product['description'], cat, product['views'])
    
    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Product.objects.filter(category=c):
            print(f'- {c}: {p}')
    
    # Generate random votes
    Vote.objects.removeAll()
    for p in Product.objects.all():
        for user in test_users:
            Vote.objects.get_or_create(voter=user, votee=p, positivity=random.choice([True, False]))

    # Add news items
    newsroom = [{'title': 'GadgetGateway is launched!', 'content': 'This website is already launched! Yay!'}]

    for piece in newsroom:
        add_news(piece['title'], piece['content'])

    for n in News.objects.all():
        print(f'{n} is added.')
    
def add_category(name):
    temp = Category.objects.get_or_create(name=name)[0]
    return temp

def add_product(name, description, category, views=0):
    temp = Product.objects.get_or_create(name=name, category=category)[0]
    temp.description = description
    temp.views = views
    temp.save()
    return temp

def add_news(title, content, date=datetime.now()):
    temp = News.objects.get_or_create(title=title, content=content)[0]
    temp.content = content
    temp.date = date
    temp.save()
    return temp

def create_test_users(number: int):
    output: list(User) = []
    for idx in range(number):
        username = 'tester'+str(idx+1)
        user = User.objects.get_or_create(username=username, email=username+'@example.com', password='00000000')[0]
        output.append(user)
    return output


# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()