from django.urls import path, include
from .views import get_routes

urlpatterns = [
    path('', get_routes, name='get_routes'),
    path('category/', include('base.url.category_urls')),
    path('course/', include('base.url.course_urls')),
    path('student/', include('base.url.student_urls')),
    path('teacher/', include('base.url.teacher_urls')),
    path('user/', include('base.url.user_urls')),
]