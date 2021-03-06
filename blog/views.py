from django.shortcuts import render, redirect, get_object_or_404
from blog.models import *
from blog.forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from django.db.models import Q
import json

def Home(request):

    if request.is_ajax() and request.method == "POST":

        if 'like' in request.POST:
            post = Post.objects.get(id=request.POST["post_id"])
            user = get_object_or_404(User, id=request.user.id)
            like_post(post=post, user=user)

            data = [{}]
            response = JsonResponse(json.dumps(data, sort_keys=True, default=str, indent=4), safe=False)
            return response

        elif 'unlike' in request.POST:
            post = Post.objects.get(id=request.POST["post_id"])
            user = get_object_or_404(User, id=request.user.id)
            delete_like(post=post, user=user)

            data = [{}]
            response = JsonResponse(json.dumps(data, sort_keys=True, default=str, indent=4), safe=False)
            return response

        elif 'comment_like' in request.POST:
            c = Comment.objects.get(id=request.POST["comment_id"])
            c.likes.add(request.user.id)

            data = [{}]
            response = JsonResponse(json.dumps(data, sort_keys=True, default=str, indent=4), safe=False)
            return response

        elif 'comment_unlike' in request.POST:
            c = Comment.objects.get(id=request.POST["comment_id"])
            c.likes.remove(request.user.id)

            data = [{}]
            response = JsonResponse(json.dumps(data, sort_keys=True, default=str, indent=4), safe=False)
            return response

        elif 'post_remove' in request.POST:
            post = Post.objects.get(id=request.POST["post_id"])
            post.delete()

            data = [{}]
            response = JsonResponse(json.dumps(data, sort_keys=True, default=str, indent=4), safe=False)
            return response

        elif 'add_comment' in request.POST:
            post = Post.objects.get(id=request.POST["comment_post_id"])
            create_comment(post=post, author=request.user, content=request.POST["content"])

            data = [{}]
            response = JsonResponse(json.dumps(data, sort_keys=True, default=str, indent=4), safe=False)
            return response

    else:
        posts = Post.objects.order_by('-date_posted')
        users = User.objects.all()
        user_count = User.objects.count()
        comments = Comment.objects.all()

        context = {
            'title': 'Home',
            'posts': posts,
            'users': users,
            'user_count': user_count,
            'comments': comments,
        }
        return render(request, "blog/home.html", context)

def Login(request):

    if request.user.is_authenticated:
        messages.error(request, "You already logged in!")
        return redirect("profile", request.user.id)

    else:
        form = ""

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, "Successfully signed in!")
                return redirect("profile", user.id)
            else:
                form = LoginForm()
                messages.error(request, "Wrong credentials!")
        else:
            form = LoginForm()

        context = {
            'form': form, 
            'title': 'Login',
        }
        return render(request, "blog/login.html", context)

def Register(request):

    if request.user.is_authenticated:
        messages.error(request, "You are logged in!")
        return redirect("profile", request.user.id)

    else:

        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)

            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                username = form.cleaned_data.get('username')
                user = User.objects.get(username=username)
                birth_date = form.cleaned_data.get('birth_date') 
                image = form.cleaned_data.get('image') 
                gender = form.cleaned_data.get('gender')
                country = form.cleaned_data.get('country')
                create_profile(user, birth_date, image, country, gender)
                messages.success(request, "Account successfully created!")
                return redirect("login")
        else:
            form = RegisterForm()

        context = {
            'form': form,
            'title': 'Register',
        }
        return render(request, "blog/register.html", context)


#
# Create, Delete Functions
#

def create_profile(user, birth_date, image, country, gender):
    u = Profile(user=user, birth_date=birth_date, image=image, country=country, gender=gender)
    u.save()

def create_post(author, content):
    p = Post(author=author, content=content)
    p.save()

def create_friendship(user, friend):
    f = Friend(user=user, friend=friend)
    f.save()

def delete_friendship(user, friend):
    f = Friend.objects.filter(user=user, friend=friend)
    f.delete()

def create_comment(post, author, content):
    p = Comment(post=post, author=author, content=content)
    p.save()

def like_post(post, user):
    l = Like(post=post, user=user)
    l.save()

def delete_like(post, user):
    l = Like.objects.filter(post=post, user=user)
    l.delete()

@login_required
def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect("home")

@login_required
def Profile_view(request, user_id):
    view_user = get_object_or_404(User, pk=user_id)
    profile = request.user.profile        

    if request.is_ajax() and request.method == "POST":

        if 'like' in request.POST:
            post = Post.objects.get(id=request.POST["post_id"])
            user = get_object_or_404(User, id=request.user.id)
            like_post(post=post, user=user)

            data = [{}]
            response = JsonResponse(json.dumps(data, sort_keys=True, default=str, indent=4), safe=False)
            return response

        elif 'unlike' in request.POST:
            post = Post.objects.get(id=request.POST["post_id"])
            user = get_object_or_404(User, id=request.user.id)
            delete_like(post=post, user=user)

            data = [{}]
            response = JsonResponse(json.dumps(data, sort_keys=True, default=str, indent=4), safe=False)
            return response

        elif 'comment_like' in request.POST:
            c = Comment.objects.get(id=request.POST["comment_id"])
            c.likes.add(request.user.id)

            data = [{}]
            response = JsonResponse(json.dumps(data, sort_keys=True, default=str, indent=4), safe=False)
            return response

        elif 'comment_unlike' in request.POST:
            c = Comment.objects.get(id=request.POST["comment_id"])
            c.likes.remove(request.user.id)

            data = [{}]
            response = JsonResponse(json.dumps(data, sort_keys=True, default=str, indent=4), safe=False)
            return response

        elif 'post_remove' in request.POST:
            post = Post.objects.get(id=request.POST["post_id"])
            post.delete()

            data = [{}]
            response = JsonResponse(json.dumps(data, sort_keys=True, default=str, indent=4), safe=False)
            return response

        elif 'add_comment' in request.POST:
            post = Post.objects.get(id=request.POST["comment_post_id"])
            create_comment(post=post, author=request.user, content=request.POST["content"])

            data = [{}]
            response = JsonResponse(json.dumps(data, sort_keys=True, default=str, indent=4), safe=False)
            return response

    if request.method == "POST":
        img_form = ProfileImgForm(request.FILES, request.POST, instance=profile)
        bg_form = ProfileBgForm(request.FILES, request.POST, instance=profile)
        bio_form = ProfileBioForm(request.POST, instance=profile)
        intro_form = ProfileIntroForm(request.POST, instance=profile)

        if 'imgbutton' in request.POST:
            if img_form.is_valid():
                if os.path.isfile(f"{profile.image}"):
                    os.remove(profile.image.path)

                if "image" in request.FILES:
                    profile.image = request.FILES["image"]
                    img_form.save()
                    messages.success(request, "Successfully changed image!")
                    return HttpResponseRedirect(request.path_info)

                else:
                    messages.error(request, "You need to upload an image!")
                    return HttpResponseRedirect(request.path_info)

            else:
                messages.error(request, "Error while changing image!")
                return HttpResponseRedirect(request.path_info)
        
        elif 'bgbutton' in request.POST:
            if bg_form.is_valid():
                if os.path.isfile(f"{profile.background}"):
                    os.remove(profile.background.path)

                if "background" in request.FILES:
                    profile.background = request.FILES["background"]
                    bg_form.save()
                    messages.success(request, "Successfully changed background!")
                    return HttpResponseRedirect(request.path_info)
                    
                else:
                    messages.error(request, "You need to upload an image!")
                    return HttpResponseRedirect(request.path_info)

            else:
                messages.error(request, "Error while changing background!")
                return HttpResponseRedirect(request.path_info)
        
        elif 'biobutton' in request.POST:
            if bio_form.is_valid():
                profile.bio = request.POST["bio"]
                bio_form.save()
                messages.success(request, "Successfully changed bio!")
                return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request, "Error while changing bio!")
                return HttpResponseRedirect(request.path_info)
        
        elif 'introbutton' in request.POST:
            if intro_form.is_valid():
                profile.birth_date = request.POST["birth_date"]
                profile.gender = request.POST["gender"]
                profile.country = request.POST["country"]
                intro_form.save()
                messages.success(request, "Successfully changed intro!")
                return HttpResponseRedirect(request.path_info)
            
            else:
                messages.error(request, "Error while changing intro")
                return HttpResponseRedirect(request.path_info)
        
        elif 'addfriend' in request.POST:
            create_friendship(user=request.user, friend=view_user)
            messages.success(request, f"Successfully added {view_user}!")
            return HttpResponseRedirect(request.path_info)
        
        elif 'removefriend' in request.POST:
            delete_friendship(user=request.user, friend=view_user)
            messages.success(request, f"Successfully removed {view_user}!")
            return HttpResponseRedirect(request.path_info)

        elif 'commentbutton' in request.POST:
            post = get_object_or_404(Post, id=request.POST["post_id"])
            create_comment(post=post, author=request.user, content=request.POST["content"])
            messages.success(request, f"Successfully created a comment!")
            return HttpResponseRedirect(request.path_info)
        

    else:

        img_form = ProfileImgForm(instance=request.user)
        bg_form = ProfileBgForm(instance=profile)
        bio_form = ProfileBioForm(instance=profile)
        intro_form = ProfileIntroForm(instance=profile)

        friends = Friend.objects.filter(Q(user=view_user) | Q(friend=view_user)).all()
        friends_count = Friend.objects.filter(Q(user=view_user) | Q(friend=view_user)).count()
        is_friend = Friend.objects.filter(Q(user=view_user, friend=request.user) | Q(user=request.user, friend=view_user)).exists()

        users = User.objects.all()
        posts = Post.objects.filter(author=view_user).order_by('-date_posted')
        liked_posts = Like.objects.filter(user=view_user).all()

        comments = Comment.objects.all()

        context = {
            'user_id': user_id,
            'title': 'Profile',
            'view_user': view_user,
            'img_form': img_form,
            'bg_form': bg_form,
            'bio_form': bio_form,
            'intro_form': intro_form,
            'users': users,
            'posts': posts,
            'comments': comments,
            'friends': friends,
            'is_friend': is_friend,
            'friends_count': friends_count,
            'liked_posts': liked_posts,
            'now': timezone.now,        
        }
        return render(request, "blog/profile.html", context)

@login_required
def Profile_settings(request):
    UserForm = UserUpdateForm(instance=request.user)
    ProfileForm = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'Profile Update',
        'uform': UserForm,
        'pform': ProfileForm,
    }
    return render(request, "blog/settings.html", context)

#@login_required



def Posts(request):
    blogs = Post.objects.all()

    context = {
        'blogs': blogs,
        'title': 'Posts',
    }

    return render(request, "blog/posts.html")









@login_required
def Post_settings(request, id):
    post = Post.objects.get(id=id)

    if request.method == "POST":
        form = UpdatePost(request.POST, instance=post)
        if form.is_valid():
            post.content = request.POST["content"]
            form.save()
            messages.success(request, "Successfully updated your post!")
            return redirect("profile", request.user.id)
        else:
            messages.error(request, "Error while updating!")
            return HttpResponseRedirect(request.path_info)
    else:
        form = UpdatePost(instance=post)

        context = {
            'title': 'Post Settings',
            'form': form,
        }
        return render(request, "blog/post_settings.html", context)

@login_required
def Friends_view(request):

    friends = Friend.objects.filter(Q(user=request.user) | Q(friend=request.user)).all()
    friends_count = Friend.objects.filter(Q(user=request.user) | Q(friend=request.user)).count()

    context = {
        'title': 'Friends',
        'friends': friends,
        'friends_count': friends_count,
    }
    return render(request, "blog/friends.html", context)
