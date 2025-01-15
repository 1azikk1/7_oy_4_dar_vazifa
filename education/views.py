from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.urls import reverse_lazy
from .models import Course, Student
from .forms import CourseForm, LoginForm, RegisterForm, StudentForm, EmailForm
from django.contrib import messages
from django.core.mail import send_mail
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Class views
# -----------------------------------------------------------------------------------


class HomeListView(ListView):
    model = Student
    template_name = 'news/courses.html'
    context_object_name = 'students'
    extra_context = {
        'title': "Asosiy Sahifa"
    }
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['courses'] = Course.objects.all()
        return context


class CourseDetailView(DetailView):
    model = Course
    pk_url_kwarg = 'course_id'
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['course'] = get_object_or_404(Course, pk=self.kwargs.get('course_id'))
        context['title'] = f'{self.object.title}: {self.object.description}'
        return context


class AddCourseView(CreateView):
    model = Course
    template_name = 'add_course.html'
    form_class = CourseForm
    extra_context = {'title': "Kurs qo'shish"}

    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'course_id': self.object.id})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Kurs muvaffaqiyatli tarzda qo'shildi!")
        return response


class UpdateCourseView(UpdateView):
    model = Course
    pk_url_kwarg = 'course_id'
    template_name = 'add_course.html'
    form_class = CourseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = f'{self.object.title}: yangilash!'
        return context

    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'course_id': self.object.id})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Kurs muvaffaqiyatli tarzda yangilandi!")
        return response


class DeleteCourseView(DeleteView):
    model = Course
    pk_url_kwarg = 'course_id'
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = f"{self.object.title}: o'chirish!"
        return context

    def get(self, request, *args, **kwargs):
        messages.warning(request, "Ushbu kursni o'chirishni xohlaysizmi?")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Kurs muvaffaqiyatli tarzda o'chirildi!")
        return response


class StudentDetailView(DetailView):
    model = Student
    pk_url_kwarg = 'student_id'
    template_name = 'student_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['student'] = get_object_or_404(Student, pk=self.kwargs.get('student_id'))
        context['title'] = f'Talaba:{self.object.name}'
        return context


class AddStudentView(CreateView):
    model = Student
    template_name = 'add_student.html'
    form_class = StudentForm
    extra_context = {
        'title': "Talaba qo'shish"
    }

    def get_success_url(self):
        return reverse_lazy('student_detail', kwargs={'student_id': self.object.id})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Talaba muvaffaqiyatli tarzda qo'shildi!")
        return response


class UpdateStudentView(UpdateView):
    model = Student
    template_name = 'add_student.html'
    form_class = StudentForm
    pk_url_kwarg = 'student_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = f'{self.object.name}: tahrirlash!'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Talaba muvaffaqiyatli tarzda tahrirlandi!")
        return response


class DeleteStudentView(DeleteView):
    model = Student
    pk_url_kwarg = 'student_id'
    template_name = 'delete_confirm_student.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = f"{self.object.name}: o'chirish!"
        return context

    def get(self, request, *args, **kwargs):
        messages.warning(request, "Ushbu talabani o'chirishni xohlaysizmi?")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Talaba muvaffaqiyatli tarzda o'chirildi!")
        return response


class SendMessageView(View):
    def get(self, request):
        form = EmailForm()
        context = {
            'form': form,
            'title': "Xabar yuborish"
        }
        return render(request, 'email.html', context)

    def post(self, request):
        form = EmailForm(data=request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            users = User.objects.all()
            for user in users:
                send_mail(
                    subject,
                    message,
                    'ahmadjonovazizbek2007@gmail.com',
                    [user.email],
                    fail_silently=False
                )
            messages.success(request, "Xabar muvaffaqiyatli tarzda yuborildi!")
            return redirect('home')

        context = {
            'form': form,
        }
        return render(request, 'email.html', context)


class StudentsByCoursesView(HomeListView):
    model = Student
    template_name = 'news/index.html'
    context_object_name = 'students'
    paginate_by = 3

    def get_queryset(self):
        students = get_list_or_404(Student, course_id=self.kwargs.get('course_id'))
        return students

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        course = get_object_or_404(Course, pk=self.kwargs.get('course_id'))
        context['course'] = course
        context['title'] = f"{course.title}: Barcha talabalar!"
        return context


# auth
class UserRegisterView(View):
    def get(self, request):
        form = RegisterForm()
        context = {
            'form': form,
            'title': "Ro'yhatdan o'tish"
        }
        return render(request, 'auth/register.html', context)

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"{user.username} tabriklaymiz, muvaffaqiyatli tarzda ro'yhatdan o'tdingiz!")
            return redirect('user_login')
        context = {
            'form': form,
            'title': "Ro'yhatdan o'tish"
        }
        return render(request, 'auth/register.html', context)


class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form': form,
            'title': "Saytga kirish"
        }
        return render(request, 'auth/login.html', context)

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            messages.success(request, f"{user.username} web sahifamizga xush kelibsiz!")
            login(request, user)
            return redirect('home')

        context = {
            'form': form,
            'title': "Saytga kirish"
        }
        return render(request, 'auth/login.html', context)


class UserLogOutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Siz web sahifamizdan chiqib ketdingiz!")
        return redirect('user_login')


class NotFoundView(View):
    def get(self, request):
        return render(request, '404.html', status=404)
