from django.urls import path ,include
from django.contrib.auth import views as auth_views
from . import views
app_name='users'
urlpatterns = [
   
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/logged_out/'), name='logout'),
    
]