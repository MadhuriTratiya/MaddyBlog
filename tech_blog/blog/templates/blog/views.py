from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Post
from .models import Post, Category



def home(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    # This line was causing the error because Category wasn't imported
    categories = Category.objects.all() 
    
    return render(request, 'blog/home.html', {
        'posts': posts,
        'categories': categories
    })
    
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    posts = Post.objects.filter(author=user)

    total_posts = posts.count()

    oracle_posts = posts.filter(
        Q(category__name__icontains="oracle")
    ).count()

    database_posts = posts.filter(
        Q(category__name__icontains="database")
    ).count()
    context = {
        'profile_user': user,
        'posts': posts,
        'total_posts': total_posts,
        'oracle_posts': oracle_posts,
        'database_posts': database_posts,
    }

    return render(request, 'blog/profile.html', context)

def category_posts(request, category_name):
    """
    This function handles clicks on the menu items.
    It filters the blog posts based on the category clicked.
    """
    # 1. Fetch the category object (e.g., 'Oracle')
    category = get_object_or_404(Category, name=category_name)
    
    # 2. Filter posts belonging to this category
    posts = Post.objects.filter(category=category, is_published=True).order_by('-created_at')
    
    # 3. We still need all categories to keep the top menu visible
    categories = Category.objects.all()
    
    return render(request, 'blog/home.html', {
        'posts': posts,
        'categories': categories,
        'active_category': category_name  # Used to highlight the active menu item
    })