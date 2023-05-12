from django.http import HttpResponseRedirect
from .models import Question, Choice, Comment, Notification
from django import forms
from .forms import QuestionForm, ChoiceForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from users.models import UserProfile


from django.shortcuts import render, reverse

# Create your views here.
def index(request):
    latest_questions = Question.objects.order_by("-pub_date")[:10]

    return render(request, "poll/index.html", {"questions": latest_questions})

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
        selected_choice_pk = request.POST['option_pk']
        
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
        return HttpResponseRedirect(reverse('poll:index'))
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
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    notifications = Notification.objects.filter(owner=user_profile)

    return render(
        request, 
        "poll/notifications.html", 
        {"notifications": notifications}
        )

