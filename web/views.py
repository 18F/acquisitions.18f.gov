from datetime import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from news.models import News


# Create your views here.
def index(request):
    news = News.objects.get(draft=False, publication_date__lte=datetime.now())
    return render(request, 'web/index.html', {'news': news})


def guides(request):
    return render(request, 'web/guides.html')


@login_required
def profile(request):
    return render(request, 'web/profile.html')


@login_required
def refresh_token(request):
    # TODO: Updating in place seems better, but couldn't get that to work.
    # Commented lines below are what I tried.
    token = Token.objects.get_or_create(user=request.user)[0]
    # token.key = token.generate_key()
    # token.save(update_fields=['key'])
    token.delete()
    Token.objects.create(user=request.user)
    return redirect("/profile/")
