from django.views.generic import TemplateView
from django.urls import path
from .views import (SendMessageView, HomeListView, CourseDetailView, StudentDetailView,AddCourseView, AddStudentView,
                    UpdateCourseView, UpdateStudentView, DeleteCourseView, DeleteStudentView, StudentsByCoursesView,
                    UserRegisterView, UserLoginView, UserLogOutView, NotFoundView)


urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('send/email/', SendMessageView.as_view(), name='send_message'),

    # course
    path('course/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/add/', AddCourseView.as_view(), name='add_course'),
    path('course/<int:course_id>/update/', UpdateCourseView.as_view(), name='update_course'),
    path('course/<int:course_id>/delete/', DeleteCourseView.as_view(), name='delete_course'),

    # student
    path('student/<int:student_id>/', StudentDetailView.as_view(), name='student_detail'),
    path('student/add/', AddStudentView.as_view(), name='add_student'),
    path('student/<int:student_id>/update/', UpdateStudentView.as_view(), name='update_student'),
    path('student/<int:student_id>/delete/', DeleteStudentView.as_view(), name='delete_student'),
    path('students/<int:course_id>/', StudentsByCoursesView.as_view(), name='students_by_course'),

    # auth
    path('auth/register/', UserRegisterView.as_view(), name='user_register'),
    path('auth/login/', UserLoginView.as_view(), name='user_login'),
    path('auth/logout/', UserLogOutView.as_view(), name='user_logout'),

    # about
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),

    # 404
    path('404/notfound/', NotFoundView.as_view(), name='404'),
]
