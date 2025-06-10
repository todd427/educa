from rest_framework import generics
from courses.api.serializers import SubjectSerializer, CourseSerializer, ModuleSerializer
from django.db.models import Count
from courses.models import Subject, Course, Module
from courses.api.pagination import StandardPagination
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer  # ✅ This line is required
    serializer = SubjectSerializer
    pagination_class = StandardPagination

class CourseDetailView(APIView):
    serializer_class = CourseSerializer
    def post(self, request, pk, format=None):   
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})
    

