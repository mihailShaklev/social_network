
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<int:profileId>", views.follow, name="follow"),
    path("unfollow/<int:profileId>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("save", views.save_post, name="save"),
    path("like", views.like, name="like"),
    path("dislike", views.dislike, name="dislike")
]
