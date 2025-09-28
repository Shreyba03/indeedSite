from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Job, Profile, Application, Skill, Experience
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

def index(request):
    jobs = Job.objects.all()
    template_data = {'jobs': jobs}
    return render(request, 'jobs/index.html', {'template_data': template_data})

def show(request, id):
    job = Job.objects.get(id=id)
    template_data = {}
    template_data['job'] = job
    template_data['title'] = job.name
    
    # Check if user has applied to this job
    if request.user.is_authenticated:
        try:
            application = Application.objects.get(user=request.user, job=job)
            template_data['application'] = application
        except Application.DoesNotExist:
            template_data['application'] = None
    
    return render(request, 'jobs/show.html', {'template_data': template_data})

@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user has already applied
    application, created = Application.objects.get_or_create(
        user=request.user,
        job=job,
        defaults={'status': 'applied'}
    )
    
    return redirect('jobs.show', id=job_id)

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)
    for skill in profile.skill_list.all():
        print(skill.name)

    for experience_list in profile.experience_list.all():
        print(experience_list.company)
    
    # Get user's applications
    applications = Application.objects.filter(user=user).select_related('job')
    
    # Parse skills from text field (comma-separated)
    '''
    skills_list = []
    if profile.skills:
        skills_list = [skill.strip() for skill in profile.skills.split(',') if skill.strip()]
    ''' 

    template_data = {}
    template_data['profile'] = profile
    template_data['owner'] = user
    template_data['applications'] = applications
    template_data['skills_list'] = profile.skill_list.all()
    template_data['experience_list'] = profile.experience_list.all()
    
    return render(request, 'jobs/profile.html', {'template_data': template_data})

@login_required
def edit_profile(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)

    if request.user != profile.user:
        return redirect('profile.index', user_id=request.user.id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile.index', user_id=request.user.id)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'jobs/edit_profile.html', {'template_data': {'form': form}})

@login_required
def edit_skills(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)

    if request.user != profile.user:
        return redirect('home.index')

    skills = profile.skill_list.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        proficiency = request.POST.get('proficiency', 'Intermediate')

        if name:
            Skill.objects.create(profile=profile, name=name, proficiency=proficiency)

        return redirect('skills.edit', user_id=profile.user.id)

    return render(request, 'jobs/edit_skills.html', {'profile': profile, 'skills': skills})


@login_required
def edit_experience(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)

    if request.user != profile.user:
        return redirect('home.index')

    experiences = profile.experience_list.all()

    if request.method == 'POST':
        company = request.POST.get('company')
        position = request.POST.get('position')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_current = request.POST.get('is_current') == 'on'

        if company and position and start_date:
            Experience.objects.create(
                profile=profile,
                company=company,
                position=position,
                description=description,
                start_date=start_date,
                end_date=end_date or None,
                is_current=is_current
            )

        return redirect('experience.edit', user_id=profile.user.id)

    return render(request, 'jobs/edit_experience.html', {'profile': profile, 'experiences': experiences})