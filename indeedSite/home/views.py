from django.shortcuts import render
from django.contrib.auth.models import User
from jobs.models import Profile

# Create your views here.
def index(request):
    users = User.objects.all()
    template_data = {}
    template_data["users"] = users
    if (request.user.is_authenticated):
        template_data["profile"] = request.user.profile
    else:
        template_data["profile"] = None
    return render(request, 'home/index.html', {"template_data": template_data})