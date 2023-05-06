from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from users.forms import SignUpForm
from poll.models import Question, Choice
from .models import UserProfile, User
from django.shortcuts import get_object_or_404


""" # Create your views here.
def index(request):
 """    


# Profile page views
def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    #Get user's followers
    user_followers = user_profile.followers.all()

    #Get user's questions
    user_questions = Question.objects.filter(author = user_profile)
    return render(request, 'users/user.html', {
        'user': user,
        'questions': user_questions,
        "followers": user_followers

    })


#Login user
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("poll:index"))
        else:
            return render(request, "users/login.html", {
                'message': "Invalid credientials"
            })
        
    return render(request, "users/login.html")

#Logout view
def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        'message': 'Logged Out' 
        })


#User profile
def profile(request, username):

    if username  == 'AnonymousUser':
        return HttpResponseRedirect(reverse(f"users:login"))
    
    if username in ['logout', 'login', 'signup']:
        return HttpResponseRedirect(reverse(f"users:{username}"))
    
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user= user)

    #Get user's followers
    user_followers = user_profile.followers.all()

    #Get user's questions
    user_questions = Question.objects.filter(author = user_profile)
    return render(request, 'users/user.html', {
        'user': user,
        'questions': user_questions,
        "followers": user_followers

    })





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




#Follow view
def connect(request, user_id):
    '''
    This function gets the signed in user, gets the user to be followed using the 
    user_id provided and adds the user to the followers or removes the user from 
    the list of folowers '''
    auth_user = get_object_or_404(UserProfile, user=request.user)
    followee = get_object_or_404(UserProfile, pk=user_id)


    if followee.followers.filter(user=request.user).exists():
        #Unfollow
        followee.followers.remove(auth_user)
    else:
        #follow
        followee.followers.add(auth_user)
    
    
    followee.save()
    return HttpResponseRedirect(reverse("poll:index"))