from django.urls import path
from ..view.teacher_views import TeacherLoginView, get_teachers, get_teacher, \
    get_teacher_profile, update_teacher_profile, make_teacher, \
    update_teacher, delete_teacher, confirm_teacher

urlpatterns = [
    path('', get_teachers, name='get_teachers'),
    path('<str:pk>/', get_teacher, name='get_teacher'),
    path('profile/', get_teacher_profile, name='get_teacher_profile'),
    path('login/', TeacherLoginView.as_view(), name='TeacherLoginView'),
    path('make/', make_teacher, name='make_teacher'),
    path('confirm/<str:pk>/', confirm_teacher, name='confirm_teacher'),
    path('profile/update/', update_teacher_profile, name='update_teacher_profile'),
    path('update/<str:pk>/', update_teacher, name='update_user'),
    path('delete/<str:pk>/', delete_teacher, name='delete_user'),
]