import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from gadgetgateway.models import Category, Product

def populate():
    laptop_products = [
        {'name': '13-inch M1 MacBook Pro',
         'description': 'The new MacBook Pro without a new design, featuring the first Apple Silicon chip.',
         'votes': 1000,
         'views': 2500},
        {'name': '2020 16-inch MacBook Pro',
         'description': 'The 16-inch MacBook Pro released in 2020. It is commonly mentioned as the last MacBook Pro with an Intel chip.',
         'votes': 600,
         'views': 0},
         {'name': '16-inch M1 MacBook Pro',
         'description': 'The new MacBook Pro without a new design, featuring the first Apple Silicon chip.',
         'votes': 1000,
         'views': 0},
        {'name': '2020 16-inch MacBook Pro',
         'description': 'The 16-inch MacBook Pro released in 2020. It is commonly mentioned as the last MacBook Pro with an Intel chip.',
         'votes': 600,
         'views': 0},
    ]

    smartphone_products = [
        {'name': 'iPhone 12 mini',
         'description': 'iPhone 12 mini is commonly named the smallest phone in 2020.',
         'votes': 1020,
         'views': 2000},
        {'name': 'iPhone 12 Pro Max',
         'description': 'iPhone 12 Pro Max is the best phone Apple have made so far.',
         'votes': 1000,
         'views': 50},
    ]

    wearable_products = [
        {'name': 'Apple Watch Series 6',
         'description': 'The Apple Watch Series 6 features a faster S6 chip and blood oxygen level tracking.',
         'votes': 1720,
         'views': 0},
        {'name': 'Huawei Watch 3 Pro',
         'description': 'Continuous Health Monitoring | Up to 14-Day Battery Life | Independent Calling',
         'votes': 1214,
         'views': 0},
    ]

    headphone_products = [
        {'name': 'Sony MDR-1AM2',
         'description': 'Affordable and approachable, the Sony MDR-1AM2 is a great starting pair of audiophile headphones',
         'votes': 720,
         'views': 60},
        {'name': 'AirPods Pro',
         'description': 'AirPods Pro earphones featuring noise canceling technology, a new design, improved water resistance, and a $249 price tag',
         'votes': 1214,
         'views': 0},
    ]

    categories = {'Laptops': laptop_products, 'Smartphones': smartphone_products, 'Wearables': wearable_products, 'Headphones': headphone_products}

    for category, data in categories.items():
        cat = add_category(category)
        for product in data:
            add_product(product['name'], product['description'], cat, product['votes'], product['views'])
    
    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Product.objects.filter(category=c):
            print(f'- {c}: {p}')
    
def add_category(name):
    temp = Category.objects.get_or_create(name=name)[0]
    temp.save()
    return temp

def add_product(name, description, category, votes=0, views=0):
    temp = Product.objects.get_or_create(name=name, category=category)[0]
    temp.description = description
    temp.votes = votes
    temp.views = views
    temp.save()
    return temp

# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()