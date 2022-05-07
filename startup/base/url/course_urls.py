from django.urls import path
from ..view.course_views import get_courses, get_course, make_course, confirm_course, update_course, delete_course

urlpatterns = [
    path('', get_courses, name='get_courses'),
    path('<str:pk>/', get_course, name='get_course'),
    path('make/', make_course, name='make_course'),
    path('confirm/<str:pk>/', confirm_course, name='confirm_course'),
    path('update/<str:pk>/', update_course, name='update_course'),
    path('delete/<str:pk>/', delete_course, name='delete_course'),
]