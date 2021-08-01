import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from gadgetgateway.models import Category, Product

def populate():
    laptop_products = [
        {'name': '13-inch M1 MacBook Pro',
         'description': 'The new MacBook Pro without a new design, featuring the first Apple Silicon chip.',
         'likes': 1000,
         'dislikes': 300},
        {'name': '2020 16-inch MacBook Pro',
         'description': 'The 16-inch MacBook Pro released in 2020. It is commonly mentioned as the last MacBook Pro with an Intel chip.',
         'likes': 600,
         'dislikes': 900}
    ]

    smartphone_products = [
        {'name': 'iPhone 12 mini',
         'description': 'iPhone 12 mini is commonly named the smallest phone in 2020.',
         'likes': 1020,
         'dislikes': 1},
        {'name': 'iPhone 12 Pro Max',
         'description': 'iPhone 12 Pro Max is the best phone Apple have made so far.',
         'likes': 1000,
         'dislikes': 900}
    ]

    categories = {'Laptop': laptop_products, 'Smartphone': smartphone_products}


    for category, data in categories.items():
        cat = add_category(category)
        for product in data:
            add_product(product['name'], product['description'], cat, product['likes'], product['dislikes'])
    
    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Product.objects.filter(category=c):
            print(f'- {c}: {p}')
    
def add_category(name):
    temp = Category.objects.get_or_create(name=name)[0]
    temp.save()
    return temp

def add_product(name, description, category, likes=0, dislikes=0):
    temp = Product.objects.get_or_create(name=name, category=category)[0]
    temp.description = description
    temp.likes = likes
    temp.dislikes = dislikes
    temp.save()
    return temp

# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()
