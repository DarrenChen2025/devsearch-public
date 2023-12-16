from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required #blocks any features that require the user to be logged in
from django.db.models import Q
from .utils import searchProjects, paginateProjects
from django.contrib import messages

def projects(request):
    projects, search_query = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 6)
    
    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST': #if the form is submitted
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount #update the vote count

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=projectObj.id)

    print(projectObj.vote_ratio)
    tags = projectObj.tags.all()
    return render(request, 'projects/single-project.html', {'project': projectObj, 'tags': tags, 'form': form})

@login_required(login_url='login') #if the user is not logged in, redirect to the login page
def createProject(request):
    profile = request.user.profile #get the profile of the user that is logged in
    form = ProjectForm()

    if request.method == 'POST': #if the form is submitted
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ProjectForm(request.POST, request.FILES) #create a new form with the data that the user submitted
        if form.is_valid(): #if the form is valid, check all the fields is correctly filled out
            project = form.save(commit=False) #save the form, into the database
            project.owner = profile #set the owner of the project to the profile of the user that is logged in
            project.save() #save the project to the database
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account') #redirect to the projects page
    
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk) #get the project of the user that is logged in
    form = ProjectForm(instance=project)  #populates the form with the data from the project

    if request.method == 'POST': #if the form is submitted the request method will be POST
        newtags = request.POST.get('newtags').replace(',', " ").split() #get the new tags from the form

        form = ProjectForm(request.POST, request.FILES, instance=project) #create a new form with the data that the user submitted
        if form.is_valid(): 
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    
    context = {'form': form, 'project': project}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete_template.html', context)