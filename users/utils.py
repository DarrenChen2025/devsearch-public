from .models import Profile, Skill
from projects.models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query) #get all the skills from the database in a list that contain the search query in the name field
    
    #get all the profiles from the database in a list that contain the search query in the fields specified
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | 
                                      Q(short_intro__icontains=search_query) | 
                                      Q(skill__in=skills)) 
    return profiles, search_query

def paginateProfiles(request, profiles, results):
    page = request.GET.get('page') #get the page number from the url
    paginator = Paginator(profiles, results) #create a paginator object with the profiles and the number of results per page

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger: #if the page is not in the url set the page number to 1
        page = 1
        profiles = paginator.page(page)
    except EmptyPage: #if the page number is greater than the number of pages, set the page number to the last page
        page = paginator.num_pages #get the total number of pages
        profiles = paginator.page(page)

    custom_range = paginator.get_elided_page_range(number=page, on_each_side=2, on_ends=1)
    
    return custom_range, profiles

def searchProjects(request):
    search_query = ''
    profile = request.user.profile

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    

    projects = profile.project_set.all()
    
    tags = Tag.objects.filter(project__in=projects, name__icontains=search_query)

    projects = projects.distinct().filter(Q(title__icontains=search_query) |
                                          Q(description__icontains=search_query) |
                                          Q(tags__in=tags))
    
    return projects, search_query

def paginateProjects(request, projects, results):
    page = request.GET.get('page') #get the page number from the url
    paginator = Paginator(projects, results) #create a paginator object with the profiles and the number of results per page

    try:
        projects = paginator.page(page)
    except PageNotAnInteger: #if the page is not in the url set the page number to 1
        page = 1
        projects = paginator.page(page)
    except EmptyPage: #if the page number is greater than the number of pages, set the page number to the last page
        page = paginator.num_pages #get the total number of pages
        projects = paginator.page(page)

    custom_range = paginator.get_elided_page_range(number=page, on_each_side=2, on_ends=1)
    
    return custom_range, projects