from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import reading_history_view
from .views import generate_summary_view
from .views import ArticleDetailView
from .views import ArticleListView
app_name = 'news'

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('', views.home, name='home'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('reading-history/', reading_history_view, name='reading_history'),  # ✅ function-based view
    path('', views.ArticleListView.as_view(), name='home'),
    path('article/<int:pk>/feedback/', views.submit_summary_feedback, name='submit_summary_feedback'),
    path('article/<int:pk>/generate-summary/', generate_summary_view, name='generate_summary'),
     
]
