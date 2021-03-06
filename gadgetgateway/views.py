from typing import Tuple
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify, truncatechars
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from gadgetgateway.forms import ProductForm , UserForm, UserProfileForm, CommentForm
from gadgetgateway.models import Category, Comment, Product, News, Vote
from datetime import datetime

# Create your views here.
def index(request):
    most_liked = sorted(Product.objects.all(), key= lambda t: t.get_satisfactory_rate())
    most_liked.reverse()
    most_liked = most_liked[:5]

    most_viewed = Product.objects.order_by('-views')[:5]

    context_dict = {'most_liked': most_liked, 'most_viewed': most_viewed}

    # Call the helper function to handle the cookies
    visitor_cookie_handler(request)

    # Obtain our Response object early so we can add cookie information.
    response = render(request, 'gadgetgateway/index.html', context=context_dict)

    # Return response back to the user, updating any cookies that need changed.
    return response


def about(request):
    context_dict = {'visits': request.session['visits']}
    return render(request, 'gadgetgateway/about.html', context=context_dict)

def news(request):
    context_dict = {'news_items': News.objects.all()}
    return render(request, 'gadgetgateway/news.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        products_list = Product.objects.filter(category=category)

        products_list = sorted(products_list, key=lambda t: t.get_satisfactory_rate())
        products_list.reverse()

        # Pagination logic
        page_number = request.GET.get('page', 1)
        paginator = Paginator(products_list, 9)
        page_obj = paginator.get_page(page_number)
        products = paginator.page(page_number)
        
        context_dict['category'] = category
        context_dict['products'] = products
        context_dict['page_obj'] = page_obj

    except Category.DoesNotExist or PageNotAnInteger or EmptyPage:
        context_dict['category'] = None
        context_dict['products'] = None

    return render(request, 'gadgetgateway/category.html', context=context_dict)

@login_required
def add_product(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/gadget-gateway/')

    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.save()
                return redirect(reverse('gadgetgateway:show_category', kwargs={'category_name_slug': category_name_slug}))

        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'gadgetgateway/add_product.html', context=context_dict)


# Login System

def register(request):
    # Boolean to tell the template if the registration was successful
    registered = False

    if request.method == 'POST':
        # Grab raw information
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # if the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save user info to the database
            user = user_form.save()

            # hash password, once hashed, update user password
            user.set_password(user.password)
            user.save()

            # since we need to set the user attribute ourselves
            # we set commit = False, this delays saving the model
            # until we're ready, helps in avoiding integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # If the user has provided a profile picture, get it from
            # the input form and put it in UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # saving UserProfile model instance
            profile.save()

            # update variable to indicate that the registration
            # was successsful
            registered = True
            return redirect(reverse('gadgetgateway:login'))

        else:
            # Invalid forms? print errors to the terminal
            print(user_form.errors, profile_form.errors)


    # Not a POST request, render our form using two ModelForm instances
    # these forms will be blank, ready for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render template depending on the context
    return render(request, 'gadgetgateway/register.html', 
    context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    # If the request is POST, get relevant information
    if request.method == 'POST':
        # Gather username and password provided by the user.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check if username/password combination is valid
        # if yes, a user object is returned
        user = authenticate(username=username, password=password)

        # If we have a user object and the details are correct
        if user:

            # Is the account active?
            if user.is_active:
                # If the user is valid and active, allow login
                login(request, user)
                return redirect(reverse('gadgetgateway:index'))

            else:
                return HttpResponse("Your rango account is disabled.")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    # If the form is not post, display the login form
    else:
        return render(request, 'gadgetgateway/login.html')


@login_required
def restricted(request):
    return render(request, 'gadgetgateway/restricted.html')

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Logout the last logged in user
    logout(request)
    # Redirect to homepage
    return redirect(reverse('gadgetgateway:index'))


# Visitor count

# Helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits

def search(request):
    results = []
    
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            results = sorted(Product.objects.filter(name__icontains=query), key= lambda t: t.get_satisfactory_rate())
            results.reverse()
            
    return render(request, 'gadgetgateway/search.html', {'results': results})

def view_product(request, product_name_slug, category_name_slug):

    try:
        category = Category.objects.get(slug=category_name_slug)
        product = get_object_or_404(Product, slug=product_name_slug)
        product.views += 1
        product.save()
        comments = Comment.objects.filter(product=product, active=True)
        user = request.user
        new_comment = None
        all_votee = Vote.objects.filter(votee=product).all()
        can_like = True
        reaction_ed = ""

        if user.is_authenticated:
            vote = all_votee.filter(voter=user)
            if vote:
                if vote.all()[0].positivity == True:
                    reaction_ed = 'liked'
                else:
                    reaction_ed = 'disliked'
                can_like = False

        # Comment posted
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.product = product
                new_comment.user = request.user
                new_comment.save()
        else:
            comment_form = CommentForm()

    except Category.DoesNotExist or Product.DoesNotExist:
        {
            "category": None,
            "product": None,
            "comments": None,
            "new_comment": None,
            "comment_form": None,
            "user": None,
            "total_likes": None,
            "no_vote": None,
            "reaction_ed": None
        }

    return render(request, 'gadgetgateway/product_detail.html', {
            "category": category,
            "product": product,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
            "user": user,
            "total_likes": product.get_satisfactory_rate(),
            "no_vote": can_like,
            "reaction_ed": reaction_ed
        })


def like_product(request, category_name_slug, product_name_slug):
    product = get_object_or_404(Product, slug=request.POST.get('product_name_slug'))
    user = request.user

    like = Vote.objects.get_or_create(votee=product, voter=user, positivity=True)[0]
    like.save()

    return HttpResponseRedirect(reverse('gadgetgateway:view_product', 
        kwargs={"product_name_slug": product_name_slug, "category_name_slug": category_name_slug}))

def dislike_product(request, category_name_slug, product_name_slug):
    product = get_object_or_404(Product, slug=request.POST.get('product_name_slug'))
    user = request.user

    like = Vote.objects.get_or_create(votee=product, voter=user, positivity=False)[0]
    like.save()

    return HttpResponseRedirect(reverse('gadgetgateway:view_product', 
        kwargs={"product_name_slug": product_name_slug, "category_name_slug": category_name_slug}))

def undo_reactions(request, category_name_slug, product_name_slug):
    product = get_object_or_404(Product, slug=request.POST.get('product_name_slug'))
    user = request.user
    Vote.objects.filter(voter=user, votee=product).delete()
    return HttpResponseRedirect(reverse('gadgetgateway:view_product', 
        kwargs={"product_name_slug": product_name_slug, "category_name_slug": category_name_slug}))