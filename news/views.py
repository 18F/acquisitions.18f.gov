from datetime import datetime
from dateutil.tz import tzlocal
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from news.models import Post


# Create your views here.
def posts(request):
    posts = Post.objects.filter(
        draft=False,
        publication_date__lte=datetime.now(tzlocal())
    ).order_by('publication_date')
    return render(request, "news/posts.html", {"posts": posts})


def post(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        draft=False,
        publication_date__lte=datetime.now(tzlocal()),
    )
    return render(request, "news/post.html", {'post': post})
