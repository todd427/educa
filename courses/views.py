from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from .models import Course, Module, Content, Subject
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.apps import apps
from django.forms.models import modelform_factory
from .forms import ModuleFormSet
from django.db.models import Count
from django.views.generic.detail import DetailView
from students.forms import CourseEnrollForm

class CourseDetailView(DetailView):
    template_name = 'courses/course/detail.html'
    model = Course
    context_object_name = 'course'

    def get_queryset(self):
        return Course.objects.select_related('subject')

    def get_object(self):
        subject_slug = self.kwargs['subject']
        course_slug = self.kwargs['slug']
        return get_object_or_404(
            self.get_queryset(),
            subject__slug=subject_slug,
            slug=course_slug
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object}
        )
        return context

  
class CourseListView(TemplateResponseMixin, View):
    template_name = 'courses/course/list.html'
    model = Course
    def get_permission_required(self):
        return []  # ✅ Disable permission checking

    def get(self, request, subject=None):
      subject = cache.get('all_subjects')
      if not subject:
        subject = Subject.objects.annotate(
            total_courses=Count('courses')
        )
        cache.set('all_subjects', subject)

    
      all_courses = Course.objects.annotate(total_modules=Count('modules'))
      if subject:
        subject = get_object_or_404(Subject, slug=subject)
        key = f'subject_{subject.id}_courses'
        courses = cache.get(key)
        if not courses:
          courses = all_courses.filter(subject=subject)
          cache.set(key, courses)
      else:
        courses = cache.get('all_courses')
        if not courses:
          courses = all_courses.all()
          cache.set('all_courses', courses)
      return self.render_to_response({
        'subjects': subjects,
        'subject': selected_subject,
        'courses': courses
        })

    
class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_to_response({'saved': 'OK'})
    
class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(order=order)
        return self.render_to_response({'saved': 'OK'})
    
class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)
    
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():  
            formset.save()
            return redirect('courses:manage_course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})
    
class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(
                app_label='courses',
                model_name=model_name
            )
        return None
    
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)
    
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name) 
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)
    
    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})
    
    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = self.request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module, item=obj)
            return redirect('courses:module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})
    
class ContentDeleteView(DeleteView):
    template_name = 'courses/manage/content/delete.html'
    permission_required = 'courses.delete_content'
    
class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
    
class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('courses:manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'

class OwnerCourseEditMixin(OwnerCourseMixin,OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'

class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'
    
class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(
            Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})
    
class ContentDeleteView(DeleteView):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('courses:module_content_list', module.id)
    