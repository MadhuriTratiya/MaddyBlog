from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.utils.text import slugify

# Imports from your local app
from .models import Post, Category, PostView, Profile, ProfileLink
from .forms import UserUpdateForm, ProfileUpdateForm, ProfileLinkFormSet

# --- Signals ---
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

# --- 1. Home Page Logic ---
def home(request):
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
        latest_updates = user_posts[:3]
        all_posts = user_posts
        profile_user = request.user 
    else:
        latest_updates = Post.objects.none()
        all_posts = Post.objects.none()
        profile_user = None

    categories = Category.objects.all()

    context = {
        'all_posts': all_posts,
        'latest_updates': latest_updates,
        'categories': categories,
        'profile_user': profile_user, 
    }
    return render(request, 'blog/home.html', context)

# --- 2. Authentication Logic ---
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.POST.get('remember_me'):
                request.session.set_expiry(1209600) # 2 weeks
            else:
                request.session.set_expiry(0) 
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

# --- 3. Post Creation & Management ---
@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        base_slug = slugify(title)
        unique_slug = f"{base_slug}-{str(uuid.uuid4())[:4]}"
        
        Post.objects.create(
            title=title,
            content=content,
            author=request.user,
            slug=unique_slug,
            is_published=True
        )
        
        messages.success(request, "Article published successfully!")
        return redirect('library')
        
    return render(request, 'blog/create_post.html')

@login_required
def toggle_publish(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.is_published = not post.is_published
    post.save()
    # Redirect back to the library
    return redirect('library')

def post_detail(request, username, slug):
    post = get_object_or_404(Post, author__username=username, slug=slug)
    
    # Simple View Tracking
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    browser = "Other"
    if "Chrome" in user_agent: browser = "Chrome"
    elif "Firefox" in user_agent: browser = "Firefox"
    elif "Safari" in user_agent: browser = "Safari"
    elif "Edge" in user_agent: browser = "Edge"

    PostView.objects.create(
        post=post,
        browser=browser,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    return render(request, 'blog/post_detail.html', {'post': post})

# --- 4. Content Filtering & Library ---
@login_required
def library(request):
    # This filters ONLY the logged-in user's posts for their library
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    context = {
        'posts': user_posts,
        'profile_user': request.user # Crucial for sidebar logic
    }
    return render(request, 'blog/library.html', context)

def category_posts(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    posts = Post.objects.filter(category=category, is_published=True).order_by('-created_at')
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})

# --- 5. Dashboard / Analytics ---
@login_required
def stats_view(request):
    views_by_date = PostView.objects.filter(post__author=request.user).annotate(date=TruncDate('timestamp')) \
        .values('date') \
        .annotate(count=Count('id')) \
        .order_by('date')

    browser_stats = PostView.objects.filter(post__author=request.user).values('browser') \
        .annotate(count=Count('id')) \
        .order_by('-count')

    context = {
        'dates': [v['date'].strftime('%d %b') for v in views_by_date if v['date']],
        'counts': [v['count'] for v in views_by_date],
        'browser_stats': browser_stats,
        'profile_user': request.user
    }
    return render(request, 'blog/stats.html', context)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.warning(request, "Post deleted.")
    return redirect('library')

# --- 6. Profile Logic ---
@login_required
def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        link_formset = ProfileLinkFormSet(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid() and link_formset.is_valid():
            u_form.save()
            p_form.save()
            link_formset.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user_profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        link_formset = ProfileLinkFormSet(instance=request.user.profile)

    return render(request, 'blog/profile_edit.html', {
        'u_form': u_form, 
        'p_form': p_form,
        'link_formset': link_formset,
        'profile_user': request.user
    })

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    
    # We removed the "if owner" logic. 
    # Now EVERYONE (including you) only sees published posts on this page.
    posts = Post.objects.filter(author=user, is_published=True).order_by('-created_at')
    
    return render(request, 'blog/user_posts.html', {'profile_user': user, 'posts': posts})
    