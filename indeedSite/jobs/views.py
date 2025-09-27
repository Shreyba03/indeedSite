from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Job, Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

# Create your views here.
def index(request):
    return render(request, 'jobs/index.html', {'template_data': {}})

def show(request, id):
    job = Job.objects.get(id=id)
    template_data = {}
    template_data['title'] = job.name
    return render(request, 'jobs/show.html', {'template_data': template_data})

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)
    template_data = {}
    template_data['profile'] = profile
    template_data['owner'] = user
    return render(request, 'jobs/profile.html', {'template_data':template_data})

@login_required
def edit_profile(request, user_id):
    profile = get_object_or_404(Profile, user__id = user_id)

    if (request.user != profile.user):
        return redirect('profile.index', user_id = request.user.id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile.index', user_id = request.user.id)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'jobs/edit_profile.html', {'template_data': {'form': form}})

    



# @login_required
# def edit_review(request, id, review_id):
#     review = get_object_or_404(Review, id=review_id)
#     if request.user != review.user:
#         return redirect('movies.show', id=id)
#     if request.method == 'GET':
#         template_data = {}
#         template_data['title'] = 'Edit Review'
#         template_data['review'] = review
#         return render(request, 'movies/edit_review.html',
#             {'template_data': template_data})
#     elif request.method == 'POST' and request.POST['comment'] != '':
#         review = Review.objects.get(id=review_id)
#         review.comment = request.POST['comment']
#         review.save()
#         return redirect('movies.show', id=id)
#     else:
#         return redirect('movies.show', id=id)
