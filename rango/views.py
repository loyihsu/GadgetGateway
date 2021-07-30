from django.http.response import HttpResponse
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.shortcuts import redirect, render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    # Call the helper function to handle the cookies
    visitor_cookie_handler(request)
    # Obtain our Response object early so we can add cookie information.
    response = render(request, 'rango/index.html', context=context_dict)

    # Return response back to the user, updating any cookies that need changed.
    return response


def about(request):
    context_dict = {'visits': request.session['visits']}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['pages'] = pages

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    return render(request, 'rango/category.html', context=context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category in the DB
            form.save(commit=True)

            # After saving the new category, redirect the user back to index view.
            return redirect('/rango/')

        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))

        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


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

        else:
            # Invalid forms? print errors to the terminal
            print(user_form.errors, profile_form.errors)


    # Not a POST request, render our form using two ModelForm instances
    # these forms will be blank, ready for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render template depending on the context
    return render(request, 'rango/register.html', 
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
                return redirect(reverse('rango:index'))

            else:
                return HttpResponse("Your rango account is disabled.")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    # If the form is not post, display the login form
    else:
        return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Logout the last logged in user
    logout(request)
    # Redirect to homepage
    return redirect(reverse('rango:index'))


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