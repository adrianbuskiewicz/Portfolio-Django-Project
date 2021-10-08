from django.urls import path
from .views import register_user_view, login_user_view, logout_user_view

app_name = 'members'

urlpatterns = [
    path('register-user/', register_user_view, name='register_user'),
    path('login/', login_user_view, name='login_user'),
    path('logout/', logout_user_view, name='logout_user'),
]
