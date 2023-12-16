from django.contrib import admin

# Register your models here.
from .models import Project, Review, Tag


admin.site.register(Project) #this will add the Project model to the admin page
admin.site.register(Review)
admin.site.register(Tag)