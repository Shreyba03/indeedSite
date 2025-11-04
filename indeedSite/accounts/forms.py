from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from jobs.models import Profile

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))
class CustomUserCreationForm(UserCreationForm):
    is_recruiter = forms.BooleanField(
        required=False,
        label="Are you a recruiter?",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    company = forms.CharField(
        required=False,
        label="Company Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_company'})
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.is_recruiter = self.cleaned_data['is_recruiter']
        if profile.is_recruiter:
            profile.company = self.cleaned_data['company']
        profile.save()
        return user