from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from users.forms import SignUpForm
from poll.models import Question, Choice
from .models import UserProfile

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_questions = Question.objects.filter(author = user_profile)
    return render(request, 'users/user.html', {
        'user': user,
        'questions': user_questions

    })

    
#Login user
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("users:index"))
        else:
            return render(request, "users/login.html", {
                'message': "Invalid credientials"
            })
        
    return render(request, "users/login.html")

#Register new user
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            print('form saved')
            user.save()
            print('user saved')
            username = form.cleaned_data.get('username')
            #email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect(reverse("users:index"))      
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {
        'form': form
    })

#Logout view
def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        'message': 'Logged Out' 
        })