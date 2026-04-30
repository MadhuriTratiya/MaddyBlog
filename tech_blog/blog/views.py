import json
import uuid
import os
import google.generativeai as genai  # Stable version for Python 3.13 stability
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm # Removed default UserCreationForm
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import default_storage

# Imports from your local app (Added CustomUserCreationForm)
from .models import Post, Category, PostView, Profile, ProfileLink
from .forms import PostForm, UserUpdateForm, ProfileUpdateForm, ProfileLinkFormSet, CustomUserCreationForm

# --- 1. AI & Modern Editor logic ---

# TODO: Ensure your API key is set here!
genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")
model = genai.GenerativeModel('gemini-1.5-flash')

@csrf_exempt
def ai_correct_content(request):
    """Uses Gemini to polish technical blog content."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_text = data.get("content", "")
            prompt = (
                "Act as a technical editor for a Senior Database Administrator. "
                "Correct grammar and spelling while maintaining technical accuracy "
                "for terms like RMAN, RAC, and OCI. Return ONLY corrected HTML."
                f"\n\nContent: {user_text}"
            )
            response = model.generate_content(prompt)
            return JsonResponse({"corrected_text": response.text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def tinymce_upload_image(request):
    """Handles 'This PC' image uploads for TinyMCE."""
    if request.method == "POST":
        file_obj = request.FILES.get('file')
        if file_obj:
            # Saves to 'media/blog_images/'
            file_name = default_storage.save(os.path.join('blog_images', file_obj.name), file_obj)
            file_url = settings.MEDIA_URL + file_name
            
            # TinyMCE requires this specific 'location' key
            return JsonResponse({'location': file_url})
            
    return JsonResponse({'error': 'Upload failed'}, status=400)

# --- 2. Signals ---

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

# --- 3. Core Pages ---

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
    return render(request, 'blog/home.html', {
        'all_posts': all_posts,
        'latest_updates': latest_updates,
        'categories': categories,
        'profile_user': profile_user, 
    })

# --- 4. Post Management ---

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # Unique slug generation
            post.slug = f"{slugify(post.title)}-{str(uuid.uuid4())[:4]}"
            post.author = request.user
            post.is_published = True
            post.save()
            messages.success(request, "Article published successfully!")
            return redirect('library')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form, 'edit_mode': False})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, "Unauthorized.")
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated successfully!")
            return redirect('post_detail', username=post.author.username, slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create_post.html', {'form': form, 'edit_mode': True})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.warning(request, "Post deleted.")
    return redirect('library')

@login_required
def toggle_publish(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.is_published = not post.is_published
    post.save()
    return redirect('library')

def post_detail(request, username, slug):
    post = get_object_or_404(Post, author__username=username, slug=slug)
    # Basic view tracking
    PostView.objects.create(post=post, ip_address=request.META.get('REMOTE_ADDR'))
    return render(request, 'blog/post_detail.html', {'post': post})

# --- 5. Library & Stats ---

@login_required
def library(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/library.html', {'posts': user_posts, 'profile_user': request.user})

@login_required
def stats_view(request):
    views_by_date = PostView.objects.filter(post__author=request.user).annotate(date=TruncDate('timestamp')) \
        .values('date').annotate(count=Count('id')).order_by('date')
    
    context = {
        'dates': [v['date'].strftime('%d %b') for v in views_by_date if v['date']],
        'counts': [v['count'] for v in views_by_date],
        'profile_user': request.user
    }
    return render(request, 'blog/stats.html', context)

# --- 6. Profile & Authentication ---
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        link_formset = ProfileLinkFormSet(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid() and link_formset.is_valid():
            u_form.save(); p_form.save(); link_formset.save()
            return redirect('user_profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        link_formset = ProfileLinkFormSet(instance=request.user.profile)

    return render(request, 'blog/profile_edit.html', {
        'u_form': u_form, 'p_form': p_form, 'link_formset': link_formset, 'profile_user': request.user
    })

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user, is_published=True).order_by('-created_at')
    return render(request, 'blog/user_posts.html', {'profile_user': user, 'posts': posts})

@login_required
def site_settings_view(request):
    # Get the existing settings for this specific user
    settings_obj = get_object_or_404(SiteSettings, user=request.user)

    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Your blog settings have been updated!")
            return redirect('site_settings')
    else:
        form = SiteSettingsForm(instance=settings_obj)

    return render(request, 'blog/settings_dashboard.html', {'form': form})