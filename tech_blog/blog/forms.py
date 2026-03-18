from django import forms
from django.contrib.auth.models import User
from .models import Profile, ProfileLink
from django.forms import inlineformset_factory

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        # Removed 'image' and 'bio' from here because they are in the Profile model
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'image', 'interests', 'highest_qualification', 'gender', 
            'city', 'town', 'state', 'country', 'occupation', 
            'skills', 'industry', 'bio'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 10, 'class': 'form-control', 'placeholder': 'Write your full bio here...'}),
            'skills': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}), # This ensures the "Choose File" button appears nicely
        }

# Formset for handling multiple Website URLs
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