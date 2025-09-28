from django import forms
from .models import Profile, Skill, Experience

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['headline', 'education', 'email', 'portfolio', 'github', "phone_number", "show_email", "show_phone"]
        

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'proficiency']
        

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'position', 'description', 'start_date', 'end_date', 'is_current']
        