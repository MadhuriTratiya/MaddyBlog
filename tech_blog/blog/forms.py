from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  # <-- Added for the registration form
from django.forms import inlineformset_factory
from tinymce.widgets import TinyMCE
from ckeditor_uploader.widgets import CKEditorUploadingWidget 
from django_summernote.widgets import SummernoteWidget
from .models import Profile, ProfileLink, Post

# --- 1. Registration Form (NEW) ---
class CustomUserCreationForm(UserCreationForm):
    # Add the email field explicitly and make it required
    email = forms.EmailField(required=True, help_text="Required for password resets.")

    class Meta:
        model = User
        fields = ("username", "email") 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

# --- 2. Post Form ---
class PostForm(forms.ModelForm):
    # This ensures the 'content' field uses the TinyMCE editor
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Post
        # Change 'category' to 'labels' (or whatever you named it in models.py)
        fields = ['title', 'content', 'labels']
        
# --- 3. User Update Form ---
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# --- 4. Profile Update Form ---
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # FIXED: 'theme_color' has been removed from this list
        fields = ['image', 'professional_title', 'bio']
        
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'professional_title': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
# --- 5. Profile Link Formset ---
ProfileLinkFormSet = inlineformset_factory(
    Profile, 
    ProfileLink, 
    fields=('url_name', 'url'), 
    extra=1, 
    can_delete=True,
    widgets={
        'url_name': forms.TextInput(attrs={'placeholder': 'e.g. LinkedIn', 'class': 'form-control'}),
        'url': forms.URLInput(attrs={'placeholder': 'https://...', 'class': 'form-control'}),
    }
)