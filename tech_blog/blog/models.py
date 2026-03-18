from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

# 1. Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_featured = models.BooleanField(default=False)
    
    # New Field: Stores labels/keywords as a string (e.g., "python, django, web")
    labels = models.CharField(max_length=100, blank=True, help_text="Enter comma separated labels")
    
    # This links the post to a specific user
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    
    # Toggle for visibility
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Basic slugify; consider adding a unique ID if titles repeat
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
# 3. User Profile Model
# 3. User Profile Model
# 3. User Profile Model
class Profile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer not to say', 'Prefer not to say'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    # REMOVED max_length to allow unlimited text
    bio = models.TextField(blank=True) 

    # Personal Information
    interests = models.CharField(max_length=255, blank=True)
    highest_qualification = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    
    # Location Information
    city = models.CharField(max_length=100, blank=True)
    town = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    # Additional Work Information
    occupation = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True, help_text="List your technical skills")
    industry = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# New Model to allow multiple URLs per user
class ProfileLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='links')
    url_name = models.CharField(max_length=100)
    url = models.URLField(max_length=255)

    def __str__(self):
        return f"{self.url_name} ({self.profile.user.username})"
       
#Create the Analytics Model 
class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
    timestamp = models.DateTimeField(auto_now_add=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    os = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"View for {self.post.title} at {self.timestamp}"