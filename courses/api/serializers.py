from rest_framework import serializers
from courses.models import Subject, Course, Module
from django.db.models import Count

class SubjectSerializer(serializers.ModelSerializer):
    total_courses = serializers.IntegerField()
    popular_courses = serializers.SerializerMethodField()
    def get_popular_courses(self, obj):
        courses = Course.objects.annotate(
            total_students=Count('students')
            ).order_by('total_students')[:3]
        return [f'{c.title} ({c.total_students})' for c in courses]
    
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug', 'total_courses', 'popular_courses']
        
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules']



