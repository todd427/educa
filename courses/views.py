from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Course, Module
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
    
class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class OwnerCourseMixin(OwnerMixin, OwnerEditMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    template_name = 'courses/manage/course/form.html'
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseDeleteMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/delete.html'

class OwnerCourseEditMixin(OwnerCourseMixin, CreateView):
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'

class CourseCreateView(OwnerCourseMixin, CreateView):
    permission_required = 'courses.add_course'

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(OwnerCourseDeleteMixin, DeleteView):
    permission_required = 'courses.delete_course'
        

class OwnerCourseModuleMixin(OwnerCourseMixin):
    model = Module
    fields = ['title', 'description']
    template_name = 'courses/manage/module/formset.html'

class OwnerCourseEditMixin(OwnerCourseMixin, UpdateView):
    template_name = 'courses/manage/course/form.html' 
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseDeleteMixin(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')

class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'courses/course/list.html'

class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'

class ManageCourseListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'courses/manage/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class ManageCourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'courses/manage/course/detail.html'
