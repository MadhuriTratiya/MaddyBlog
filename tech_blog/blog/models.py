import math
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField # Recommended for your AI features

# --- 1. Category Model ---
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# --- 2. Post Model (SaaS Optimized) ---
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField() # TinyMCE handles this in the frontend
    
    # SaaS & SEO Fields
    meta_description = models.CharField(max_length=160, blank=True, help_text="Short summary for Google")
    is_featured = models.BooleanField(default=False)
    labels = models.CharField(max_length=100, blank=True, help_text="Comma separated labels")
    
    # Ownership & Status
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # SaaS best practice: Add a small random ID to slug to avoid collisions
            self.slug = f"{slugify(self.title)}-{str(uuid.uuid4())[:4]}"
        super().save(*args, **kwargs)

    def get_read_time(self):
        """Calculates reading time for the technical SaaS audience"""
        word_count = len(self.content.split())
        read_time = math.ceil(word_count / 200)
        return read_time

    def __str__(self):
        return self.title

# --- 3. SaaS SiteSettings Model ---
class SiteSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    
    # Branding
    site_name = models.CharField(max_length=100, default="My MaddyBlog")
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True)
    
    # SEO & Analytics
    meta_description = models.TextField(max_length=200, blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    
    # Toggles
    enable_newsletter = models.BooleanField(default=False)
    show_reading_time = models.BooleanField(default=True)
    custom_css = models.TextField(blank=True, help_text="Professional CSS Overrides")

    def __str__(self):
        return f"Settings for {self.user.username}"

# --- 4. User Profile Model ---
# --- 4. User Profile Model ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    professional_title = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    
    # ❌ Comment out or delete this line so Django stops looking for it in Oracle:
    # theme_color = models.CharField(max_length=7, default='#dc3545') 

    def __str__(self):
        return f'{self.user.username} Profile'

# --- 5. Profile Links (Social Hub) ---
class ProfileLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='links')
    url_name = models.CharField(max_length=100) # e.g., LinkedIn
    url = models.URLField(max_length=255)

    def __str__(self):
        return f"{self.url_name} ({self.profile.user.username})"

# --- 6. SaaS Analytics Model ---
class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
    timestamp = models.DateTimeField(auto_now_add=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    os = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"View for {self.post.title}"

# --- 7. SaaS Automation Signals ---
@receiver(post_save, sender=User)
def create_user_saas_assets(sender, instance, created, **kwargs):
    """Automatically provisions Identity and Product Config for new signups"""
    if created:
        Profile.objects.create(user=instance)
        SiteSettings.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        # This ensures every new SaaS user gets a default SiteSettings row
        SiteSettings.objects.get_or_create(user=instance)