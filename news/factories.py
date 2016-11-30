import factory
from datetime import datetime, timedelta, tzinfo
from dateutil.tz import tzlocal
from acquisitions.factories import UserFactory
from news.models import Post


class NewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker('catch_phrase')
    slug = factory.Faker('slug')
    content = factory.Faker('paragraph')
    authors = factory.RelatedFactory(UserFactory)
    publication_date = factory.Faker(
            'date_time_between_dates',
            datetime_start=datetime.now() - timedelta(days=5),
            datetime_end=datetime.now() + timedelta(days=5),
            tzinfo=tzlocal(),
        )
    draft = False
