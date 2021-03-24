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
from django.core.files.storage import default_storage

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
            create_comment(post=post, author=request.user,content=request.POST["content"])

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

    context = {}

    if request.user.is_authenticated:
        messages.error(request, "You are logged in!")
        return redirect("profile", request.user.id)

    else:

        if request.is_ajax() and request.method == "POST":

            if 'Form1' in request.POST:
                form = Register1Form(request.POST)

                if form.is_valid():
                    email, first_name, last_name = form.cleaned_data.get('email'), form.cleaned_data.get('first_name'), form.cleaned_data.get('last_name')

                    request.session["r_email"] = email
                    request.session["r_first_name"] = first_name
                    request.session["r_last_name"] = last_name

                    return JsonResponse({'message': 'success'})
                else:
                    return JsonResponse({'message': form.errors})

            elif 'Form2' in request.POST:
                form = Register2Form(request.POST, request.FILES)

                if form.is_valid():
                    birth_date, image, country, gender = form.cleaned_data.get('birth_date'), form.cleaned_data.get('image'), form.cleaned_data.get('country'), form.cleaned_data.get('gender')
                    request.session["r_profile"] = create_profile(user=None, birth_date=birth_date, image=image, country=country, gender=gender)

                    return JsonResponse({'message': 'success'})
                else:
                    return JsonResponse({'message': form.errors})

            elif 'Form3' in request.POST:
                form = Register3Form(request.POST)

                if form.is_valid():
                    email = request.session["r_email"]
                    first_name = request.session["r_first_name"]
                    last_name = request.session["r_last_name"]

                    user = form.save()
                    user.refresh_from_db()
                    user = User.objects.get(username=form.cleaned_data.get("username"))

                    User.objects.filter(username=form.cleaned_data.get("username")).update(email=email, first_name=first_name, last_name=last_name)
                    Profile.objects.filter(id=request.session["r_profile"]).update(user=user)

                    messages.success(request, "Successfully created the account!")
                    return redirect("/login/")
                else:
                    return JsonResponse({'message': form.errors})

        context = {
            "title": "Register",
            "form1": Register1Form,
            "form2": Register2Form,
            "form3": Register3Form,
        }

        return render(request, "blog/register.html", context)

#
# Create, Delete Functions
#

def create_profile(user, birth_date, image, country, gender):
    u = Profile(user=user, birth_date=birth_date,image=image, country=country, gender=gender)
    u.save()
    return u.id


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
    view_user = get_object_or_404(User, id=user_id)
    profile = request.user.profile

    if view_user:
        if request.is_ajax() and request.method == "POST":

            if 'like' in request.POST:
                post = Post.objects.get(id=request.POST["post_id"])
                user = get_object_or_404(User, id=request.user.id)
                like_post(post=post, user=user)

                data = [{}]
                response = JsonResponse(data, safe=False)
                return response

            elif 'unlike' in request.POST:
                post = Post.objects.get(id=request.POST["post_id"])
                user = get_object_or_404(User, id=request.user.id)
                delete_like(post=post, user=user)

                data = [{}]
                response = JsonResponse(data, safe=False)
                return response

            elif 'comment_like' in request.POST:
                c = Comment.objects.get(id=request.POST["comment_id"])
                c.likes.add(request.user.id)

                data = [{}]
                response = JsonResponse(data, safe=False)
                return response

            elif 'comment_unlike' in request.POST:
                c = Comment.objects.get(id=request.POST["comment_id"])
                c.likes.remove(request.user.id)

                data = [{}]
                response = JsonResponse(data, safe=False)
                return response

            elif 'new_post' in request.POST:
                create_post(author=request.user, content=request.POST["content"])

                data = [{}]
                response = JsonResponse(data, safe=False)
                return response

            elif 'post_remove' in request.POST:
                post = Post.objects.get(id=request.POST["post_id"])
                post.delete()

                data = [{}]
                response = JsonResponse(data, safe=False)
                return response

            elif 'add_comment' in request.POST:
                post = Post.objects.get(id=request.POST["comment_post_id"])
                create_comment(post=post, author=request.user, content=request.POST["content"])

                data = [{}]
                response = JsonResponse(data, safe=False)
                return response

        if request.method == "POST":
            img_form = ProfileImgForm(request.FILES, request.POST, instance=profile)
            bg_form = ProfileBgForm(request.FILES, request.POST, instance=profile)
            bio_form = ProfileBioForm(request.POST, instance=profile)
            intro_form = ProfileIntroForm(request.POST, instance=profile)

            if 'imgbutton' in request.POST:
                if img_form.is_valid():

                    if "image" in request.FILES:
                        if default_storage.exists(f"{profile.image}"):
                            default_storage.delete(f"{profile.image}")
                        
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

                    if "background" in request.FILES:
                        profile.background = request.FILES["background"]
                        bg_form.save()
                        if os.path.isfile(f"{profile.background}"):
                            os.remove(profile.background.path)
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
                create_comment(post=post, author=request.user,content=request.POST["content"])
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
            posts = Post.objects.filter(author=view_user).order_by('-date_posted').all()
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

    else:
        messages.error(request, "There is no account with that id!")
        return redirect(Home)


@login_required
def Profile_settings(request):
    if request.method == "POST":
        UserForm = UserUpdateForm(request.POST, instance=request.user)   
        ProfileForm = ProfileUpdateForm(request.POST, instance=request.user.profile)

        img_form = ProfileImgForm(request.FILES, request.POST, instance=request.user.profile)
        bg_form = ProfileBgForm(request.FILES, request.POST, instance=request.user.profile)
        
        if UserForm.is_valid():
            UserForm.save()
        else: 
            messages.error(request, "Wrong user settings!")
        
        if ProfileForm.is_valid():
            ProfileForm.save()
        else:
            messages.error(request, "Wrong profile settings!")
        
        if img_form.is_valid():

            if "image" in request.FILES:
                profile.image = request.FILES["image"]
                img_form.save()
                messages.success(request, "Successfully changed image!")
                if os.path.isfile(f"{request.user.profile.image}"):
                    os.remove(f"{request.user.profile.image.path}")

        else:
            messages.error(request, "Error while changing image!")

        if bg_form.is_valid():

            if "background" in request.FILES:
                profile.background = request.FILES["background"]
                bg_form.save()
                messages.success(request, "Successfully changed background!")
                if os.path.isfile(f"{request.user.profile.background}"):
                    os.remove(f"{request.user.profile.background.path}")

        else:
            messages.error(request, "Error while changing background!")
        
        return HttpResponseRedirect(request.path_info)

    else:
        UserForm = UserUpdateForm(instance=request.user)
        ProfileForm = ProfileUpdateForm(instance=request.user.profile)
        img_form = ProfileImgForm(instance=request.user.profile)
        bg_form = ProfileBgForm(instance=request.user.profile)

        context = {
            'title': 'Profile Update',
            'uform': UserForm,
            'pform': ProfileForm,
            'imgform': img_form,
            'bgform': bg_form,
        }
        return render(request, "blog/settings.html", context)


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

    users = User.objects.all()
    user_count = User.objects.all().count()
    friends = Friend.objects.filter(Q(user=request.user) | Q(friend=request.user)).all()
    friends_count = Friend.objects.filter(Q(user=request.user) | Q(friend=request.user)).count()

    context = {
        'title': 'Friends',
        'friends': friends,
        'friends_count': friends_count,
        'users': users,
        'user_count': user_count,
    }
    return render(request, "blog/friends.html", context)

#
# CHAT
#


@login_required
def Room_view(request, room_name):
    room = get_object_or_404(Room, title=room_name)

    if request.method != "POST":
        if room:
            if request.user in room.users.all():
                chat_messages = Message.objects.filter(room=room).all()
                context = {
                    'room': room,
                    'room_name': room_name,
                    'chat_messages': chat_messages,
                }
                return render(request, "blog/chat_room.html", context)
            else:
                messages.error(request, "You aren't to the joined to the room!")
                return redirect(Chat_view)

        else:
            messages.error(request, "There are no such room!")
            return redirect(Chat_view)
    else:
        room.users.add(request.user.id)
        context = {
            'room': room,
            'room_name': room_name,
        }
        return render(request, "blog/chat_room.html", context)

@login_required
def Chat_view(request):
    context = {}
    if request.is_ajax() and request.method == "POST":
        if "create_room" in request.POST:
            try:
                x = Room.objects.get(title=request.POST["title"])
            except Room.DoesNotExist:
                x = None
            
            if x != None:
                return JsonResponse({'message': 'alreadyExists'})
            else:
                room = Room(creator=request.user, title=request.POST["title"], limit=request.POST["limit"])
                room.save()
                room.users.add(request.user.id)
                return JsonResponse({'message': 'success'})

    if request.method == "POST":

        if "leave_room" in request.POST:
            room = Room.objects.get(id=request.POST["room_id"])
            room.users.remove(request.user.id)

            if room.users.count() == 0:
                room.delete()
        
        elif "enter_room" in request.POST:
            room = Room.objects.get(id=request.POST["room_id"])
            room.users.add(request.user.id)

    rooms = Room.objects.all().order_by("title") 

    context = {
        "title": "Chat Rooms",
        "rooms": rooms,
    }

    return render(request, "blog/chat.html", context)