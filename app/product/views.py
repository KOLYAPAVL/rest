from django.views.generic.list import ListView
from .models import Product, Category
from django.db.models import Q

# Create your views here.
class ProductList(ListView):
    model = Product
    template_name = 'product/products.html'
    
    @property
    def category(self):
        if not self.request.GET.get('category'):
            return None
        return Category.objects.filter(
            id=self.request.GET['category']
        ).first()
        
    @property
    def search(self):
        return self.request.GET.get('query')
        
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        if self.category:
            queryset = queryset.filter(category=self.category) 
        if self.search:
            queryset = queryset.filter(
                Q(description__icontains=self.search) |
                Q(name__icontains=self.search) |
                Q(category__name__icontains=self.search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['active_category'] = self.category
        context['query'] = self.search
        context['page'] = 'menu'
        return context
