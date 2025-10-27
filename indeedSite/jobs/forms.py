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
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'company': forms.TextInput(attrs={'class':'form-control'}),
            'location': forms.TextInput(attrs={'class':'form-control'}),
            'salary_min': forms.NumberInput(attrs={'class':'form-control'}),
            'salary_max': forms.NumberInput(attrs={'class':'form-control'}),
            'skills_required': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':6}),
            'remote': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'visa_sponsorship': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }


        