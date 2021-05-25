from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from music_app import UserForm, UserProfileForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index(request):
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    return render(request, 'music_app/index.html', context=context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.save()
                registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
        'rango/register.html',
        {'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                login(request, user)
                return redirect(reverse('music_app:index'))
            else:
                return HttpResponse("Your music_app account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
# The request is not a HTTP POST, so display the login form.
# This scenario would most likely be a HTTP GET.
    else:
        return render(request, 'music_app/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('music_app:index'))
