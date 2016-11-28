from datetime import datetime, tzinfo
from dateutil.tz import tzlocal
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from news.models import Post


# Create your views here.
def index(request):
    posts = Post.objects.filter(
        draft=False,
        publication_date__lte=datetime.now(tzlocal())
    ).order_by('publication_date')[:5]
    return render(request, 'web/index.html', {'posts': posts})


def guides(request):
    return render(request, 'web/guides.html')


@api_view(['GET'])
def api(request, format=None):
    return Response({
        'projects': reverse('api:project-list', request=request, format=format),
        'buys': reverse('api:buy-list', request=request, format=format),
        'iaas': reverse('api:iaa-list', request=request, format=format),
        'team': reverse('api:team-list', request=request, format=format),
        'roles': reverse('api:role-list', request=request, format=format),
    })


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
