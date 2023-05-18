from django.http import HttpResponseRedirect
from .models import Question, Choice, Comment, Notification
from django import forms
from .forms import QuestionForm, ChoiceForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404
from users.models import UserProfile


from django.shortcuts import render, reverse

# Create your views here.
def index(request):
    user = request.user

    if user.is_authenticated:
        return HttpResponseRedirect(reverse("poll:home"))
    
    latest_questions = Question.objects.order_by("-pub_date")[:10]  
    return render(request, "poll/index.html", {"questions": latest_questions})

@login_required(login_url="users/login")
def home(request):
    this_user = get_object_or_404(UserProfile, user=request.user)
    
    following = this_user.following.all()
    feed = []
    for person in following:
        latest_polls = Question.objects.filter(author=person).order_by("-pub_date")[:5]
        for poll in latest_polls:
            feed.append(poll)

    return render(request, "poll/home.html", {'latest_following_polls': feed})


# Route to the polls details page
def poll_details(request, question_id):
    

    question = get_object_or_404(Question, pk=question_id)
    choices = question.options.all()
    poll_comments = Comment.objects.filter(question=question)

    #Increment views upon poll details page request
    #  poll.views += 1
    
    total_vote_count= 0
    for _ in choices:
        total_vote_count += _.votes

    return render(request, "poll/details.html", {
        "question": question, 
        "options": choices,
        'count': total_vote_count,
        'comments': poll_comments
    })


def search(request):
    query = request.GET['query'].capitalize()

    question_results = []
    questions = Question.objects.all()
    for question in questions:
        if query.lower() in question.question_text.lower():
            question_results.append(question)

    people_results = []
    people = UserProfile.objects.all()
    for person in people:
        if query.lower() in person.user.username.lower():
            people_results.append(person)

    choice_results = []
    choices = Choice.objects.all()
    for choice in choices:
        if query.lower() in choice.choice_text.lower():
            choice_results.append(choice)

    return render(request, "poll/search.html", {
        "question_results": question_results,
        "people_results": people_results,
        "choice_results": choice_results

        })



def send_notifcation(sender, object, action):
    #TODO Add message to object author specifying the action
    pass


@login_required(login_url='users/login')
def add_choices(request):
    question_pk = request.session["question_pk"]
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            question = get_object_or_404(Question, pk=question_pk)
            choice_text1 = form.cleaned_data.get("choice_text1")
            choice_text2 = form.cleaned_data.get("choice_text2")
            choice_text3 = form.cleaned_data.get("choice_text3")
            choice_text4 = form.cleaned_data.get("choice_text4")

            choice1 = Choice(question=question, choice_text=choice_text1)
            choice1.save()
            choice2 = Choice(question=question, choice_text=choice_text2)
            choice2.save()
            choice3 = Choice(question=question, choice_text=choice_text3)
            choice3.save()
            choice4 = Choice(question=question, choice_text=choice_text4)
            choice4.save()
        else:
            return render(
                request,
                "poll/add.choices.html",
                {"choices_forms": form, "message": "Type in valid choices"},
            )

        return HttpResponseRedirect(reverse("poll:index"))
    else:
        question = Question.objects.get(pk=question_pk)
        choice_form = ChoiceForm()
        return render(
            request,
            "poll/add_choices.html",
            {"choices_form": choice_form, "question": question},
        )

@login_required(login_url='users/login')
def add_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data.get("question_text")
            description = form.cleaned_data.get("description")
            author_profile = UserProfile.objects.get(user=request.user)

            question = Question(
                question_text=question_text,
                description=description,
                author=author_profile,
            )
            question.save()

            request.session["question_pk"] = question.pk

        else:
            return render(
                request,
                "poll/add_question.html",
                {
                    "question_form": question_form,
                    "message": "Kindly, type in a valid question",
                },
            )

        return HttpResponseRedirect(reverse("poll:add_choices"))

    else:
        question_form = QuestionForm()
        return render(
            request, "poll/add_question.html", {"question_form": question_form}
        )

@login_required(login_url='users/login')
def vote(request):
    if request.method == "POST":
        #catch the error raised if no option was selected
        try:
            selected_choice_pk = request.POST['option_pk']
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('poll:home')))
        
        option = get_object_or_404(Choice, pk=selected_choice_pk)
        question = option.question
        user = UserProfile.objects.get(user = request.user)
        
        #Check if user exists amongst voters of ALL the choices in this question
        for question_choice in question.options.all():
            if question_choice.voters.filter(user= request.user).exists():
                return HttpResponseRedirect(reverse('poll:poll_details', args=(question.pk,)))
        
        #Increment the votes and add voters if not
        option.votes += 1
        option.voters.add(user)
        option.save()

    #Add notification to poll author's notifications
    new_notification = Notification(owner=question.author, action='vote', action_receiver=question, from_who=user)
    new_notification.save()
    

    return HttpResponseRedirect(reverse('poll:poll_details', args=(question.pk,)))

def delete(request, question_id):
    #get question
    question = get_object_or_404(Question, pk=question_id)
    #if request.method == "POST":
    #Check if request.user is author
    if request.user == question.author.user:
        question.delete()
        return HttpResponseRedirect(reverse('poll:home'))
        # redirect back to the previous page
        #return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('poll:home')))
        
    else:
        return HttpResponseRedirect(reverse("poll:poll_details", args=(question_id,)))


def comment(request):
    if request.method == 'POST':
        comment_author = UserProfile.objects.get(user =request.user)
        question = Question.objects.get(pk=request.POST["question"])
        comment = Comment(comment_text=request.POST["comment_text"],  question=question, author=comment_author)
        comment.save()

    #Add notification to poll author's notifications
    new_notification = Notification(owner=question.author, action='comment', action_receiver=question, from_who=comment_author)
    new_notification.save()

    return HttpResponseRedirect(reverse("poll:poll_details", args=(question.id,)))


def like(request):
    if request.method == 'POST':
        liker = UserProfile.objects.get(user =request.user)
        question = Question.objects.get(pk=request.POST["question"])

        question.likers.add(liker)
        

    #Add notification to poll author's notifications
    new_notification = Notification(owner=question.author, action='like', action_receiver=question, from_who=liker)
    new_notification.save()

    return HttpResponseRedirect(reverse("poll:poll_details", args=(question.id,)))



@login_required(login_url='users:login')
def notifications(request):
    #get the auth'd user
    user_profile = get_object_or_404(UserProfile, user=request.user)

    notifications = Notification.objects.filter(owner=user_profile)

    return render(
        request, 
        "poll/notifications.html", 
        {"notifications": notifications}
        )

@login_required(login_url='users:login')
def activities(request):
    #get the auth'd user

    user_profile = get_object_or_404(UserProfile, user=request.user)

    activities = Notification.objects.filter(from_who=user_profile)

    return render(
        request, 
        "poll/notifications.html", 
        {"notifications": activities}
        )


def connections(request):
    # Get the signed in user
    this_user = get_object_or_404(UserProfile, user = request.user)
    
    # Get the follower and following
    user_followers = this_user.followers.all()
    user_following = this_user.following.all()

    # Return the connections page, passing in the followers and following of the user

    return render(request, 'poll/connections.html', {
        'followers': user_followers,
        'followings': user_following
    })

