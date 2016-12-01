from datetime import datetime
from dateutil.tz import tzlocal
from django.contrib.syndication.views import Feed
from django.urls import reverse
from news.models import Post


class LatestPosts(Feed):
    title = "TTS Office of Acquisitions Updates"
    link = "/news/"
    description = "Updates from the TTS Office of Acquisitions team about "\
                  "experiments, buys, events, and more"

    def items(self):
        return Post.objects.filter(
            draft=False,
            publication_date__lte=datetime.now(tzlocal()),
        ).order_by('publication_date')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content
