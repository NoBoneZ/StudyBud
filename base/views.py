from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserForm
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required




def login_page(request):
    page ="login"

    if request.user.is_authenticated:
        return redirect("base:home")

    if request.method == "POST":
        email = request.POST["email"].lower()
        password = request.POST["password"]

        try:
            username = User.objects.get(email=email)
        except:
            messages.error(request, "User doesnt exist.")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('base:home')
            
        messages.error(request, "Invalid Details")
    

    context = {"page": page}
    return render(request, "base/login_registration.html", context)


def logout_user(request):
    logout(request)
    return redirect('base:home' )


def register_user(request):
    page = "register"
    form = MyUserForm()

    if request.method == "POST":
        form = MyUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("base:home"))

        else:
            messages.error(request, "An error occurred during registration")


    context ={'form': form}
    return render (request, "base/login_registration.html", context) 

def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else " " 

    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    
    room_messages = Message.objects.filter(Q(room__name__icontains=q)| Q(room__topic__name__icontains=q)).order_by("-message_created")
    return render(request, "base/home.html", {"rooms":rooms, "topics": topics, "room_count" : room_count, "room_messages" : room_messages})

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST["body"]
        )
        room.participants.add(request.user)
        return HttpResponseRedirect(reverse("base:room", args=[room.id]))
    
    return render(request, "base/room.html", {"room":room, "room_messages": room_messages, "participants": participants})



@login_required(login_url="base:login")
def userprofile(request, pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    rooms = user.room_set.all()
    
    context = {"user" : user, "topics" : topics, "room_messages": room_messages , "rooms":rooms}
    return render(request, "base/profile.html", context)


@login_required(login_url="base:login")
def createroom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    
    if request.method == "POST":
        # form = RoomForm(request.POST)
        topic_name = request.POST["topic"]
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        
        Room.objects.create(host=request.user, topic=topic, name=request.POST["name"], description=request.POST["description"])
        

        return redirect('base:home')

    context = {'form' :form, "topics":topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="base:login")
def updateRoom(request, pk):
    room = get_object_or_404(Room,id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    task = "update"
    if request.user != room.host:
        # return HttpResponse("You are not allowed here")
        return HttpResponseForbidden(request)

    if request.method == "POST":
       topic, created = Topic.objects.get_or_create(name=request.POST["topic"])
       room.name = request.POST["name"]
       room.topic = topic
       room.description = request.POST["description"]
       room.save()
       return HttpResponseRedirect(reverse("base:home"))

    context = {"form": form, "topics": topics, 'room':room, "task":task}
    return render(request, "base/room_form.html", context)

@login_required(login_url="base:login")
def deleteRoom(request, pk):
    room = get_object_or_404(Room, id=pk)

    if request.user != room.host:
        return HttpResponseForbidden(request)

    if request.method == "POST":
        room.delete()
        return HttpResponseRedirect(reverse("base:home"))

    context = {'obj':room}
    return render(request, "base/delete.html", context)


@login_required(login_url="base:login")
def delete_message(request, pk, id):
    room = Room.objects.get(id=pk)
    message = room.message_set.all().get(id=id)
    
    
    
    if request.user != message.user:
        return HttpResponseForbidden(request)
    
    if request.method == "POST":
        message.delete()
        return HttpResponseRedirect(reverse("base:room", args=[room.id]))
    
    context = {"obj" : message}
    return render(request, "base/delete.html", context)


@login_required(login_url="base:login")
def updateuser(request, pk):
    user = get_object_or_404(User, id=pk)
    form = UserForm(instance=user)
    
    
    if request.user != user:
        return HttpResponseForbidden(request)
    
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("base:profile" ,args=[user.id]))
    
    
    context = {"form":form}
    return render(request, "base/update-user.html", context)


def topicspage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    context ={"topics": topics}
    return render(request, "base/topics.html", context)


def activitypage(request):
    room_messages = Message.objects.all()
    
    context = {"room_messages" :room_messages}
    return render(request, "base/activity.html", context)