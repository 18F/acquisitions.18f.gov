from datetime import datetime
from dateutil.tz import tzlocal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from news.models import Post


# Create your views here.
def posts(request):
    post_list = Post.objects.filter(
        draft=False,
        publication_date__lte=datetime.now(tzlocal())
    ).order_by('publication_date')
    # Pagination: https://docs.djangoproject.com/en/1.10/topics/pagination/
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, "news/posts.html", {"posts": posts})


def post(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        draft=False,
        publication_date__lte=datetime.now(tzlocal()),
    )
    return render(request, "news/post.html", {'post': post})
