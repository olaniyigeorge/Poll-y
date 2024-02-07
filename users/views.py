from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from users.forms import SignUpForm
from poll.models import Question, Notification
from .models import UserProfile, User
from django.shortcuts import get_object_or_404



# Profile page views
def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    
    return HttpResponseRedirect(reverse("users:profile", args=(request.user.username,)))



#Login user
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password= password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("poll:home"))
        else:
            return render(request, "users/login.html", {
                'message': "Invalid credientials"
            })
        
    return render(request, "users/login.html")

#Logout view
def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse("poll:index"))


#User profile
def profile(request, username):

    if username  == 'AnonymousUser':
        return HttpResponseRedirect(reverse(f"users:login"))
    
    if username in ['logout', 'login', 'signup', 'connections']:
        return HttpResponseRedirect(reverse(f"users:{username}"))
    
    
    
    auth_user_profile = get_object_or_404(UserProfile, user=request.user) 


    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user= user)

    #Get user's followers
    user_followers = user_profile.followers.all()

    #Get user's following
    user_following = user_profile.following.all()

    #Get user's questions
    #user_questions = user_profile.questions_asked.all()
    user_questions = Question.objects.filter(author = user_profile)
    return render(request, 'users/user.html', {
        'user': user,
        'user_profile': user_profile,
        'questions': user_questions,
        "followers": user_followers,
        'followings': user_following,
        'authup': auth_user_profile

    })



#Register new user
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            #TODO Refresh user from database, creating userprofile in effect 
            user = form.save()
            user.refresh_from_db()
            
            #save user
            user.save()
            
            # Get username and password for authentication
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # Log user in with username and raw password
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect(reverse("users:index"))     
        else:
            return render(request, "users/signup.html", {
        'form': form,
        'message': 'Form not valid'
    })
    else:
        form = SignUpForm()
 
    return render(request, "users/signup.html", {'form': form})


#Follow view
def connect(request, user_id):
    '''
    This function gets the signed in user, gets the user to be followed using the 
    user_id provided and adds the user to the followers or removes the user from 
    the list of folowers 
    '''
    auth_user = get_object_or_404(UserProfile, user=request.user)
    followee = get_object_or_404(UserProfile, pk=user_id)

    if followee.followers.filter(user=request.user).exists():
        #Unfollow
        followee.followers.remove(auth_user)
        
        # create unfollow notification for the appropriate users
        new_notification = Notification(owner=followee, action='unfollow', from_who=auth_user)
        new_notification.save()
    else:
        #follow
        followee.followers.add(auth_user)

        # create follow notification for the appropriate users
        new_notification = Notification(owner=followee, action='follow', from_who=auth_user)
        new_notification.save()
        
    followee.save()

    return HttpResponseRedirect(reverse("users:profile", args=(followee.user.username,)))



