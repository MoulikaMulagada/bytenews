from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'news'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
]
