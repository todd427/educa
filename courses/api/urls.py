from django.urls import path, include
from rest_framework import routers
from . import views
app_name = 'courses'
router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('subjects', views.SubjectViewSet)
urlpatterns = [
     path('', include(router.urls)),
     path('courses/<int:pk>/enroll/', views.CourseDetailView.as_view(), name='course_enroll'),
]


