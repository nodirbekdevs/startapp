from django.urls import path
from ..view.category_views import get_categories, get_category, make_category, update_category, delete_teacher

urlpatterns = [
    path('', get_categories, name='get_categories'),
    path('<str:pk>/', get_category, name='get_category'),
    path('make/', make_category, name='make_category'),
    path('update/<str:pk>/', update_category, name='update_category'),
    path('delete/<str:pk>/', delete_teacher, name='delete_teacher'),
]