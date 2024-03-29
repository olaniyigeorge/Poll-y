from django.urls import path

from . import views
from Polly import settings
from django.conf.urls.static import static

app_name = 'poll'

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("poll/<int:question_id>", views.poll_details, name="poll_details"),
    path("add_question", views.add_question, name="add_question"),
    path("add_choices/", views.add_choices, name="add_choices"),
    path('vote/', views.vote, name="vote"),
    path("delete/<int:question_id>", views.delete, name="delete"),
    path("comment", views.comment, name="comment"),
    path("like", views.like, name="like"),
    path('notifications', views.notifications, name='notifications'),
    path('notifications/activities', views.activities, name='activities'),
    path("connections", views.connections, name="connections")
] 