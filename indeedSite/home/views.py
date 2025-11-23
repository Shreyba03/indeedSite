from django.shortcuts import render
from django.contrib.auth.models import User
from jobs.models import Profile, Job

# Create your views here.
# def index(request):
#     users = User.objects.all()
#     template_data = {}
#     template_data["users"] = users
#     if (request.user.is_authenticated):
#         template_data["profile"] = request.user.profile
#     else:
#         template_data["profile"] = None
#     return render(request, 'home/index.html', {"template_data": template_data})

# def index(request):
#     users = User.objects.all()
#     template_data = {}
#     template_data["users"] = users
    
#     if request.user.is_authenticated:
#         template_data["profile"] = request.user.profile
        
#         # NEW: pass recruiter’s jobs to the home page
#         if request.user.profile.is_recruiter:
#             recruiter_jobs = Job.objects.filter(company=request.user.profile.company)
#         else:
#             recruiter_jobs = None
#     else:
#         template_data["profile"] = None
#         recruiter_jobs = None

#     return render(
#         request, 
#         'home/index.html', 
#         {
#             "template_data": template_data,
#             "recruiter_jobs": recruiter_jobs,
#         }
#     )

def index(request):
    users = User.objects.all()
    template_data = {"users": users}

    recruiter_jobs = None  # default

    if request.user.is_authenticated:
        template_data["profile"] = request.user.profile

        # For recruiters: show only THEIR jobs
        if request.user.profile.is_recruiter:
            recruiter_jobs = Job.objects.filter(posted_by=request.user.profile)
    else:
        template_data["profile"] = None

    return render(
        request,
        'home/index.html',
        {
            "template_data": template_data,
            "recruiter_jobs": recruiter_jobs,
        }
    )