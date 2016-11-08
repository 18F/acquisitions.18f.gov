from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'web/index.html')


def guides(request):
    return render(request, 'web/guides.html')


@login_required
def profile(request):
    return render(request, 'web/profile.html')
