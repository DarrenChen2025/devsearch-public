from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query) #get all the tags from the database in a list that contain the search query in the name field

    projects = Project.objects.distinct().filter(Q(title__icontains=search_query) | 
                                                 Q(description__icontains=search_query) | 
                                                 Q(owner__name__icontains=search_query) |
                                                 Q(tags__in=tags))
    
    return projects, search_query

def paginateProjects(request, projects, results):
    page = request.GET.get('page') #get the page number from the url
    paginator = Paginator(projects, results) #create a paginator object with the projects and the number of results per page

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