from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['headline', 'skills', 'education', 'experience', 'email', 'portfolio', 'github', "phone_number", "show_email", "show_phone"]
