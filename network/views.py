from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from datetime import datetime
from .models import *


def index(request):

    #Get all posts
    posts = Posts.objects.all().order_by('-time_stamp')

    #Create a paginator
    paginator = Paginator(posts, 10)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    page_object = paginator.get_page(page_number)

    #Check for likes
    if request.user.id:
        likedPosts = Likes.objects.filter(user=request.user).values_list('like', flat=True)
    else:
        likedPosts = False

    return render(request, "network/index.html", {"page_object": page_object, "likedPosts": likedPosts})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url="login")
def new_post(request):

    #Create a new post
    username = request.user.username
    if request.method == "POST":
        user = request.user
        text = request.POST["text"]
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%d %H:%M")
        likes = 0
        post = Posts(user=user,username=username,text=text,time_stamp=time_stamp,likes=likes)
        post.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new_post.html")


@login_required(login_url="login")
def profile(request, username):

    #Get the profile
    profile = User.objects.get(username=username)
    profileId = profile.id

    # Get the followed and the followers
    num_followers = profile.followed.count()
    num_followed = profile.followers.count()

    follower = Followers.objects.filter(followed=profile, follower=request.user)

    if follower:
        isFollowed = True
    else:
        isFollowed = False

    posts = profile.posts.all().order_by('-time_stamp')

    # Create paginator
    paginator = Paginator(posts, 10)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    page_object = paginator.get_page(page_number)

    # Get the likes for the user post
    if request.user.id:
        likedPosts = Likes.objects.filter(user=request.user).values_list('like', flat=True)
    else:
        likedPosts = False

    return render(request, "network/profile.html", {"profileId": profileId, "isFollowed": isFollowed,
                 "profileName": username, "followers": num_followers, "followed": num_followed, "page_object": page_object, "likedPosts": likedPosts})


# Follow a user
@login_required(login_url="login")
def follow(request, profileId):
    followed = User.objects.get(id=profileId)
    follower = request.user

    entry = Followers(followed=followed, follower=follower)
    entry.save()

    return HttpResponseRedirect(reverse('profile', args=(followed.username,)))


# Unfollow a user
@login_required(login_url="login")
def unfollow(request, profileId):
    followed = User.objects.get(id=profileId)
    follower = request.user

    query = Followers.objects.filter(followed=followed,follower=follower).delete()

    return HttpResponseRedirect(reverse('profile', args=(followed.username,)))


# Render page with user posts who the user follows
@login_required(login_url="login")
def following(request):

    # Get all the followed users by a single user and all their posts
    followedUsers = Followers.objects.filter(follower=request.user).values_list('followed', flat=True)
    followedUsersPosts = Posts.objects.filter(user__in=followedUsers).order_by('-time_stamp')

    # Create paginator
    paginator = Paginator(followedUsersPosts, 10)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    page_object = paginator.get_page(page_number)

    # Get the likes for a post
    if request.user.id:
        likedPosts = Likes.objects.filter(user=request.user).values_list('like', flat=True)
    else:
        likedPosts = False

    return render(request, "network/following.html", {"page_object": page_object, "likedPosts": likedPosts})


# Save an edited post
@csrf_exempt
@login_required(login_url="login")
def save_post(request):

    data = json.loads(request.body)
    postId = data["postId"]
    post = Posts.objects.get(id=postId)
    post.text = data["text"]
    post.save()
    return HttpResponse(status=204)


# Like a post
@csrf_exempt
@login_required(login_url="login")
def like(request):

    data = json.loads(request.body)
    postId = data["id"]
    post = Posts.objects.get(id=postId)
    post.likes += 1
    post.save()
    user = request.user
    like = Likes(user=user, like=post)
    like.save()
    return HttpResponse(status=204)


# Dislike a post
@csrf_exempt
@login_required(login_url="login")
def dislike(request):

    data = json.loads(request.body)
    postId = data["id"]
    post = Posts.objects.get(id=postId)
    post.likes -= 1
    post.save()
    user = request.user
    Likes.objects.get(user=user, like=post).delete()
    return HttpResponse(status=204)