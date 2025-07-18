from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.db.models import Q, Count
from .models import Article, Category

def home(request):
    return HttpResponse("<h1>Welcome to NewsGenie AI</h1>")

class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    ordering = ['-published_date']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category_name = self.request.GET.get('category')
        query = self.request.GET.get('q')

        if category_name:
            queryset = queryset.filter(categories__name__iexact=category_name)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(article_count=Count('article')).order_by('name')
        context['search_query'] = self.request.GET.get('q', '')
        context['current_category'] = self.request.GET.get('category', 'All')
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'
