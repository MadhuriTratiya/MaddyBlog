from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Post, Category

def home(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'blog/home.html', {
        'posts': posts,
        'categories': categories
    })

def category_posts(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    posts = Post.objects.filter(category=category, is_published=True).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'blog/home.html', {
        'posts': posts,
        'categories': categories,
        'active_category': category_name
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    categories = Category.objects.all()
    context = {
        'profile_user': user,
        'posts': posts,
        'categories': categories,
        'total_posts': posts.count(),
    }
    return render(request, 'blog/profile.html', context)