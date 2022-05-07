from django.urls import path
from ..view.student_views import get_students, get_student, get_student_profile, \
    add_course, remove_course, make_student, \
    update_student_profile, update_student, delete_student, StudentLoginView

urlpatterns = [
    path('', get_students, name='get_students'),
    path('<str:pk>/', get_student, name='get_student'),
    path('profile/', get_student_profile, name='get_student_profile'),
    path('login/', StudentLoginView.as_view(), name='StudentLoginView'),
    path('make/', make_student, name='make_student'),
    path('course_add/<str:pk>/', add_course, name='add_course'),
    path('course_remove/<str:pk>/', remove_course, name='remove_course'),
    path('profile/update/', update_student_profile, name='update_student_profile'),
    path('update/<str:pk>/', update_student, name='update_student'),
    path('delete/<str:pk>/', delete_student, name='delete_student'),
]