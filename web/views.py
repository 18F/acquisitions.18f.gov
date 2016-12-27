from datetime import datetime, tzinfo
from dateutil.tz import tzlocal
from itertools import chain
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
)
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from news.models import Post
from projects.models import IAA, Project, AgileBPA, Micropurchase


# Create your views here.
def index(request):
    posts = Post.objects.filter(
        draft=False,
        publication_date__lte=datetime.now(tzlocal())
    ).order_by('publication_date')[:5]
    return render(request, 'web/index.html', {'posts': posts})


def search(request):
    # Get search params
    terms = request.GET.get('q', '')

    posts = Post.objects.annotate(
        rank=SearchRank(
            SearchVector('title','content'),
            SearchQuery(terms),
        )
    ).filter(
        draft=False,
        publication_date__lte=datetime.now(tzlocal()),
        rank__gte=0.04
    )
    # iaas = IAA.objects.annotate(
    #
    # )
    projects = Project.objects.annotate(
        rank=SearchRank(
            SearchVector('name', 'description'),
            SearchQuery(terms)
        )
    ).filter(public=True, rank__gte=0.04)
    agilebpas = AgileBPA.objects.annotate(
        rank=SearchRank(
            SearchVector('name', 'description', 'acquisition_plan'),
            SearchQuery(terms)
        )
    ).filter(public=True, rank__gte=0.04)
    micropurchases = Micropurchase.objects.annotate(
        rank=SearchRank(
            SearchVector('name', 'description'),
            SearchQuery(terms)
        )
    ).filter(public=True, rank__gte=0.04)
    results = list(chain(
        projects,
        agilebpas,
        micropurchases,
        posts,
    ))
    return render(request, 'web/search.html', {
        'results': results
    })


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
