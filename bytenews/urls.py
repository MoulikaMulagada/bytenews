from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from news.views import ArticleListView, ArticleDetailView  # ❌ Removed `home`

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth-related URLs
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('logged_out/', TemplateView.as_view(template_name='registration/logged_out.html')),

    # App URLs
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include(('news.urls', 'news'), namespace='news')),
    # Homepage is article list
    path('', ArticleListView.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
]
