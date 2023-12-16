from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False) #only one owner for each project so many=False
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField() #we are going to use a custom method to get the reviews

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj): #self is the serializer instance, obj is the model instance
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data