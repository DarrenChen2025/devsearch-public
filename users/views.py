from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required #blocks any features that require the user to be logged in
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm #django's built in form for creating a user
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .models import Profile, Message
from .utils import searchProfiles, paginateProfiles, searchProjects, paginateProjects
from django.db import IntegrityError, transaction
# Create your views here.

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated: #if the user is already logged in, stops the user from going to the login page if they are already logged in
        return redirect('profiles') #redirect to the profiles page

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username) #if the user exists
        except:
            messages.error(request, "Username does not exist")
        
        user = authenticate(request, username=username, password=password) #authenticate the user to the database, if the user exists it returns an instance of the user, if not it returns None

        if user is not None:
            login(request, user) #the login function creates a session for the user
            messages.success(request, "You are now logged in!")
            return redirect(request.GET['next'] if 'next' in request.GET else 'account') #redirect to the profiles page
        else:
            messages.error(request, "Username OR password is incorrect")
        
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, "User was logged out!")
    return redirect('login')

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('account')
    
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Check if the email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                form.add_error('email', "Email is already in use")
            else:
                try:
                    with transaction.atomic():
                        user = form.save(commit=False)
                        user.username = user.username.lower()
                        user.save()
                        messages.success(request, "User account was created!")
                        login(request, user)
                        return redirect('edit-account')
                except IntegrityError:
                    messages.error(request, "An error has occurred during registration")
        else:
            messages.error(request, "An error has occurred during registration")

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles, search_query = searchProfiles(request) #get the profiles and the search query from the searchProfiles function in utils.py
    custom_range, profiles = paginateProfiles(request, profiles, 3) #get the custom range and the profiles from the paginateProfiles function in utils.py
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="") #exclude the skills that have no description
    otherSkills = profile.skill_set.filter(description="") #filter the skills that have no description

    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login') #if the user is not logged in, redirect to the login page
def userAccount(request):
    profile = request.user.profile #get the profile of the user that is logged in

    skills = profile.skill_set.all() #get all the skills of the user
    projects = profile.project_set.all()[:3]
    projectsCount = projects.count()

    context = {'profile': profile, 'skills': skills, 'projects': projects, 'projectsCount': projectsCount}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile #get the profile of the user that is logged in
    form = ProfileForm(instance=profile) #gets the current data of the profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile) #updates the profile with the new data
        #instance=profile is to tell django that we want to update the profile of the user that is logged in without it, it would create a new profile object
        #request.POST contain all the submitted data from the form
        #request.FILES is for the profile image
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form, }
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    form = SkillForm()
    profile = request.user.profile

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect('account')
        
    context = {'form': form,}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect('account')
        
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect('account')
    
    context = {'object': skill}
    return render(request, 'delete_template.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all() #get the recipient messages (the related_name='messages' in the Message model)
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            #if the user is logged in, we would have to manually set the name and email since in the html we set the name and email to be hidden if they are logged in
            if sender: 
                message.name = sender.name
                message.email = sender.email
            
            message.save()

            messages.success(request, "Your message was successfully sent!")
            return redirect('user-profile', pk=recipient.id)
    
    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)


@login_required(login_url='login')
def viewAllProjects(request):
    projects, search_query = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 6)

    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/all_projects.html', context)