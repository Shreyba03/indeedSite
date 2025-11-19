from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Job, Profile, Application, Skill, Experience, Message, Search
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProfileForm, JobForm, ContactCandidateForm
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
import requests
import csv
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    jobs = Job.objects.all()
    template_data = {'jobs': jobs}
    return render(request, 'jobs/index.html', {'template_data': template_data})

def show(request, id):
    job = Job.objects.get(id=id)
    template_data = {}
    template_data['job'] = job
    template_data['title'] = job.name

    if request.user.is_authenticated:
        try:
            application = Application.objects.get(user=request.user, job=job)
            template_data['application'] = application
        except Application.DoesNotExist:
            template_data['application'] = None
    
    return render(request, 'jobs/show.html', {'template_data': template_data})

# @login_required
# def apply_to_job(request, job_id):
#     job = get_object_or_404(Job, id=job_id)
    
#     application, created = Application.objects.get_or_create(
#         user=request.user,
#         job=job,
#         defaults={'status': 'applied'}
#     )
    
#     return redirect('jobs.show', id=job_id)

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)
    
    applications = Application.objects.filter(user=user).select_related('job')

    template_data = {}
    template_data['profile'] = profile
    template_data['owner'] = user
    if user == request.user:
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


def job_list(request):
    jobs = Job.objects.all()

    title = request.GET.get("title")
    skills = request.GET.get("skills")
    location = request.GET.get("location")
    remote = request.GET.get("remote")
    visa = request.GET.get("visa")
    salary_min = request.GET.get("salary_min")
    salary_max = request.GET.get("salary_max")

    if title:
        jobs = jobs.filter(title__icontains=title)
    if skills:
        jobs = jobs.filter(skills_required__icontains=skills)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if remote:
        jobs = jobs.filter(remote=True)
    if visa:
        jobs = jobs.filter(visa_sponsorship=True)
    if salary_min:
        jobs = jobs.filter(salary_min__gte=salary_min)
    if salary_max:
        jobs = jobs.filter(salary_max__lte=salary_max)

    return render(request, "jobs/job_list.html", {"jobs": jobs})


def job_detail(request, id):
    job = get_object_or_404(Job, id=id)
    return render(request, "jobs/job_detail.html", {"job": job})

@login_required
def apply_to_job(request, id):
    job = get_object_or_404(Job, id=id)

    # Check if user already applied to this job
    existing_application = Application.objects.filter(user=request.user, job=job).first()
    if existing_application:
        messages.warning(request, "You have already applied to this job.")
        return redirect("job_detail", id=job.id)

    if request.method == "POST":
        note = request.POST.get("note", "")
        Application.objects.create(user=request.user, job=job, note=note, status="Applied")
        messages.success(request, "Your application has been submitted!")
        return redirect("job_detail", id=job.id)

    return render(request, "jobs/apply.html", {"job": job})

@login_required
def my_applications(request):
    # Get all applications for the logged-in user
    applications = Application.objects.filter(user=request.user).order_by('-applied_at')
    return render(request, "jobs/my_applications.html", {"applications": applications})

@login_required
def recommended_jobs(request):
    profile = request.user.profile
    user_skills = profile.skill_list.values_list('name', flat=True)

    jobs = Job.objects.none()

    for skill in user_skills:
        jobs |= Job.objects.filter(skills_required__icontains=skill.strip())

    jobs = jobs.distinct()  # remove duplicates
    return render(request, "jobs/recommended_jobs.html", {"jobs": jobs})

def job_map_page(request):
    """Renders the HTML page containing the map."""
    return render(request, "jobs/job_map.html")

def job_map_data(request):
    """Returns JSON data for all jobs with lat/lng."""
    jobs = Job.objects.values("id", "title", "company", "location", "latitude", "longitude")
    return JsonResponse(list(jobs), safe=False)

##################################################
# RECRUITER VIEWS
##################################################

# helper function to get latitude and longitude
def get_lat_long(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    response = requests.get(url, params=params, headers={"User-Agent": "my-django-app"})
    data = response.json()
    if data:
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon
    return None, None

def create_job(request):
    if not request.user.is_authenticated:
        return redirect('accounts.login')

    profile = Profile.objects.get(user=request.user)
    if not profile.is_recruiter:
        return redirect('home.index')  # block non-recruiters

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            lat, lon = get_lat_long(job.location)
            job.latitude = lat
            job.longitude = lon
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()

    return render(request, 'jobs/create_job.html', {'form': form})

def edit_job(request, job_id):
    if not request.user.is_authenticated:
        return redirect('accounts.login')

    profile = Profile.objects.get(user=request.user)
    if not profile.is_recruiter:
        return redirect('home.index')  # block non-recruiters

    # Get the job, only allow if it belongs to the user's company
    job = get_object_or_404(Job, id=job_id, company=profile.company)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            # Optionally update lat/lon if location changed
            lat, lon = get_lat_long(job.location)
            job.latitude = lat
            job.longitude = lon
            job.save()
            return redirect('job_detail', job.id)
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {'form': form, 'job': job})

def user_list(request):
    search_term = request.GET.get('search', '')

    profiles = Profile.objects.select_related('user').prefetch_related('skill_list', 'project_list')

    if search_term:
        if request.user.is_authenticated:
            Search.objects.get_or_create(
                recruiter=request.user,
                search_term=search_term,
                defaults={'name': f"Search: {search_term}"}
            )

        profiles = profiles.filter(
            Q(user__username__icontains=search_term) |
            Q(headline__icontains=search_term) |
            Q(skill_list__name__icontains=search_term)
        ).distinct()

    template_data = {
        'title': 'User Profiles',
        'profiles': profiles,
        'search_term': search_term,
    }

    return render(request, 'jobs/user_list.html', {'template_data': template_data})

@login_required
def inbox(request, username=None):
    users = User.objects.exclude(id=request.user.id)
    selected_user = None
    messages = []

    if username:
        selected_user = get_object_or_404(User, username=username)

        if request.method == "POST":
            content = request.POST.get("message")
            if content:
                message = Message()
                message.sender = request.user
                message.receiver = selected_user
                message.content = content
                message.save()


            return redirect('job_inbox', username=selected_user.username)

        messages = Message.objects.filter(
            sender__in=[request.user, selected_user],
            receiver__in=[request.user, selected_user]
        ).order_by('timestamp')

    return render(request, 'jobs/inbox.html', {
        'users': users,
        'selected_user': selected_user,
        'messages': messages
    })

@login_required
def deleteMsg(request, username, id):
    selected_user = None

    if username:
        selected_user = get_object_or_404(User, username=username)

    message = get_object_or_404(Message, id=id)
    message.delete()
    
    return redirect('job_inbox', username=selected_user.username)

def recommended_users(request, id):
    job = get_object_or_404(Job, id=id)
    job_skills = [s.strip().lower() for s in job.skills_required.split(',')]

    recommended_profiles = []

    for profile in Profile.objects.all():
        if hasattr(profile, 'skill_list'):
            profile_skills = [s.name.lower() for s in profile.skill_list.all()]
        else:
            profile_skills = [s.strip().lower() for s in profile.skills.split(',')]

        match_count = len(set(job_skills) & set(profile_skills))
        if match_count > 0:
            profile.match_count = match_count
            recommended_profiles.append(profile)

    template_data = {
        'job': job,
        'profiles': recommended_profiles,
        'skills_required': job_skills,
        'title': f"Recommended Users for {job.title}",
        'total_matches': len(recommended_profiles),
    }

    return render(request, 'jobs/recommended_users.html', {'template_data':template_data})

@login_required
def recruiter_pipeline(request):
    """Display applications grouped by status."""
    # If recruiters have profiles with company info, filter by company
    if hasattr(request.user, 'profile') and request.user.profile.is_recruiter:
        company = request.user.profile.company
        jobs = Job.objects.filter(company=company)
        print(jobs)
        applications = Application.objects.filter(job__in=jobs)
        print(applications)
    else:
        applications = Application.objects.all()

    # Group by status
    status_groups = {}
    for code, label in Application.STATUS_CHOICES:
        status_groups[label] = applications.filter(status=code)

    print(status_groups)
    print(Application.objects.values_list('status', flat=True).distinct())


    return render(request, 'jobs/recruiter_pipeline.html', {
        'status_groups': status_groups
    })


@login_required
def update_application_status(request, app_id):
    if request.method == "POST":
        new_status = request.POST.get("status")
        app = get_object_or_404(Application, id=app_id)
        app.status = new_status
        app.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

@login_required
def send_email(request, user_id):
    recruiter_profile = Profile.objects.get(user=request.user)

    if not recruiter_profile.is_recruiter:
        return redirect('home.index')

    candidate_profile = get_object_or_404(Profile, user__id=user_id)
    print(candidate_profile.email)

    if request.method == 'POST':
        form = ContactCandidateForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            from_email = settings.DEFAULT_FROM_EMAIL  

            full_message = f"""
Message from recruiter: {recruiter_profile.email}

{message}
            """

            send_mail(
                subject,
                full_message,
                from_email,  
                [candidate_profile.email],
                fail_silently=False,
            )

            return redirect('profile.index', user_id=user_id)

    else:
        form = ContactCandidateForm()

    return render(request, 'jobs/send_email.html', {
        'form': form,
        'candidate': candidate_profile
    })

def notifications(request):
    recruiter = request.user
    searches = recruiter.saved_searches.order_by('-created_at')[:3]  # last 10 searches
    notifications = {}

    for search in searches:
        profiles = Profile.objects.select_related('user').prefetch_related('skill_list', 'project_list')

        if search.search_term:
            profiles = profiles.filter(
                Q(user__username__icontains=search.search_term) |
                Q(headline__icontains=search.search_term) |
                Q(skill_list__name__icontains=search.search_term)
            ).distinct()

        if profiles.exists():
            notifications[search] = profiles

    return render(request, 'jobs/notifications.html', {'notifications': notifications})