from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'news' # Define the namespace for this app 



urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('', views.home, name='home'),  # ✅ Built-in view
    path('', views.ArticleListView.as_view(), name='article_list'), # Our main news list page 

    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'), # New URL 

]