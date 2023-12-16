from django.forms import ModelForm
from django import forms
from .models import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'demo_link', 'source_link', 'featured_image'] #choose what fields that we want to show in the form
        widgets = {
            'tags': forms.CheckboxSelectMultiple(), #this is how we can make a checkbox
        }

    def __init__(self, *args, **kwargs): #this is how we can customize the form
        super(ProjectForm, self).__init__(*args, **kwargs)

        #method 1 of customizing the form
        #self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add Title'}) #class input is a css class


        #method 2 of customizing the form
        for k, v in self.fields.items():
            v.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }
    
    def __init__(self, *args, **kwargs): #this is how we can customize the form
        super(ReviewForm, self).__init__(*args, **kwargs)

        for k, v in self.fields.items():
            v.widget.attrs.update({'style': 'width: 100% !important;'})
        