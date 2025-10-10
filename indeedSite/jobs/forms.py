from django import forms
from .models import Profile, Skill, Experience, Job

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

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'company',
            'description',
            'location',
            'remote',
            'remote_friendly',
            'visa_sponsorship',
            'salary_min',
            'salary_max',
            'skills_required',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'skills_required': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

        