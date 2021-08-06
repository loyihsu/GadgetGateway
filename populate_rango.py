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
        {'name': '13-inch M1 MacBook Pro (2020)',
         'description': 'The new MacBook Pro without a new design, featuring the first Apple Silicon chip.',
         'views': 2520,
         },
        {'name': '2020 16-inch MacBook Pro (2020)',
         'description': 'The 16-inch MacBook Pro released in 2020. It is commonly mentioned as the last MacBook Pro with an Intel chip.',
         'views': 2880,
         },
        {'name': 'Apple MacBook Air M1 (2020)',
         'description': 'The new Apple MacBook Air (M1, 2020) is not just the best laptop Apple has ever made, it is the best laptop money can buy right now.',
         'views': 5125,
         },
         {'name': 'HP Spectre x360 14',
         'description': 'The HP Spectre x360 14 is the best 2-in-1 laptop of 2021. It’s hard to come up with a single complaint about the Spectre x360 14. It’s a drop-dead gorgeous machine with a sturdy build and a premium look and feel. ',
         'views': 3666,
         },
        {'name': 'LG Gram 17 (2021)',
         'description': 'Even if you’ve used a light laptop before, it’s difficult to explain how light the LG Gram 17 is. It has a massive 17-inch display, but it’s somehow only three pounds.',
         'views': 1452,
         },
         {'name': 'HP Envy x360 (2020)',
         'description': 'The new MacBook Pro without a new design, featuring the first Apple Silicon chip.',
         'views': 2100,
         },
        {'name': 'Razer Book 13',
         'description': 'A stylish, powerful productivity and gaming laptop. The Razer Book 13 delivers outstanding performance in an oustanding chassis.',
         'views': 2336,
         },
         {'name': 'Asus ZenBook Duo (2020)',
         'description': 'One of the best laptop concepts implementing dual screen for better producitity.',
         'views': 4336,
         }
    ]

    smartphone_products = [
        {'name': 'iPhone 12 mini',
         'description': 'iPhone 12 mini is commonly named as the best smallest phone in 2020.',
         'views': 768,
         },
        {'name': 'iPhone 12 Pro Max',
         'description': 'iPhone 12 Pro Max is the best phone Apple have made so far.',
         'views': 3880,
         },
         {'name': 'Samsung Galaxy S21 / S21 Plus',
         'description': 'Although the Samsung Galaxy S21 and S21 Plus don’t post the big numbers the S21 Ultra does, they are still picked right now for best Android phones under a thousand bucks.',
         'views': 2478,
         },
        {'name': 'Samsung Galaxy Note 20 Ultra',
         'description': 'If you’re looking for the best phone to go from morning to night with heavy use and last through it all, Samsung’s top-of-the-line Galaxy Note 20 Ultra is the one to get. .',
         'views': 2130,
         },
         {'name': 'OnePlus 9',
         'description': 'The OnePlus 9 is the step-down model from the OnePlus 9 Pro, which is itself an excellent phone. But you don’t give up too much by opting for the 9, and you save a ton of money. ',
         'views': 2000,
         },
        {'name': 'Google Pixel 4A',
         'description': 'Simlple, beautiful, affordable. The Pixel 4A’s main claim to fame is its camera, which can go head-to-head with smartphones that cost $1,500 or more.',
         'views': 1512,
         },
         {'name': 'Samsung Galaxy A52 5G',
         'description': 'The Galaxy A52 5G is our current pick for the best Android phone under $500, but it’s also worth highlighting here for its combination of features usually reserved for premium devices and a reasonable price.',
         'views': 1849,
         },
        {'name': 'Xiaomi Mi 11',
         'description': 'Mi 11 is a flagship-killing powerhouse. If the price of the latest and greatest flagships have you quaking in your boots, then the Xiaomi Mi 11 is the perfect alternative for the cost-savvy.',
         'views': 1411,
         },
         {'name': 'OnePlus Nord CE',
         'description': 'It is not as feature-rich as the OnePlus 9 Pro, but for less than half the price, the OnePlus Nord CE is astonishing value for money',
         'views': 1255,
         },
         {'name': 'Huawei Mate 40 Pro review',
         'description': 'An incredible phone, but one that’s hard to recommend. It has fantastic cameras, great design, great battery life but limited apps list.',
         'views': 880,
         }
    ]

    wearable_products = [
        {'name': 'Apple Watch Series 6',
         'description': 'The Apple Watch Series 6 features a faster S6 chip and blood oxygen level tracking. The top tier Apple Watch for those willing to spend',
         'views': 1765,
         },
        {'name': 'Huawei Watch 3 Pro',
         'description': 'Continuous Health Monitoring | Up to 14-Day Battery Life | Independent Calling',
         'views': 1376,
         },
         {'name': 'Samsung Galaxy Watch 3',
         'description': 'The best smartwatch for those on Android, and it works with iPhone too',
         'views': 1876,
         },
         {'name': 'Fitbit Versa Lite',
         'description': 'The Versa Lite has a good range of fitness features, a battery that`ll last you a good few days ',
         'views': 516,
         },
         {'name': 'Honor Magic Watch 2',
         'description': 'If you`re a fond exerciser but don`t think a dedicated sports watch is for you, then the Honor Magic Watch 2 might be the right smartwatch for you. ',
         'views': 943,
         }
    ]

    headphone_products = [
        {'name': 'Sony MDR-1AM2',
         'description': 'Affordable and approachable, the Sony MDR-1AM2 is a great starting pair of audiophile headphones',
         'views': 312,
         },
        {'name': 'AirPods Pro',
         'description': 'AirPods Pro earphones featuring noise canceling technology, a new design, improved water resistance, and a $249 price tag',
         'views': 276,
         },
         {'name': 'Sony WH-1000XM4',
         'description': 'The Sony WH-1000XM4 headphones have it all. A lightweight design, comfort, the convenience of Bluetooth and arguably the best noise-cancelling currently on the market.',
         'views': 312,
         },
        {'name': 'AKG Y400',
         'description': 'A fantastic addition to the world of wireless headphones.',
         'views': 81,
         }
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