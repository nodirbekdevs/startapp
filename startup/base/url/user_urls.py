from django.urls import path
from ..view.user_views import UserLoginView, get_users, get_user, \
    get_user_profile, update_user_profile, make_user, \
    update_user, delete_user

urlpatterns = [
    path('', get_users, name='get_users'),
    path('<str:pk>/', get_user, name='get_user'),
    path('profile/', get_user_profile, name='get_user_profile'),
    path('login/', UserLoginView.as_view(), name='UserLoginView'),
    path('make/', make_user, name='make_user'),
    path('profile/update/', update_user_profile, name='user_profile_update'),
    path('update/<str:pk>/', update_user, name='update_user'),
    path('delete/<str:pk>/', delete_user, name='delete_user'),
]