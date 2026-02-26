from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField

# 1. Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# 2. Post Model (Enhanced with CKEditor RichText)
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    # Using 'default' config from settings.py for professional formatting
    content = RichTextUploadingField(config_name='default', extra_plugins=['justify', 'font', 'codesnippet']) 
    
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# 3. User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'

# 4. Signals
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()