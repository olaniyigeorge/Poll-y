from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [

    path("", views.index, name='index'),
    path("<str:username>", views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout')
] 