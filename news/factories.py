import factory
from datetime import datetime, timedelta, tzinfo
from news.models import News


class NewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = News

    title = factory.Faker('catch_phrase')
    content = factory.Faker('paragraph')
    publication_date = factory.Faker(
            'date_time_between_dates',
            datetime_start=datetime.now() - timedelta(days=5),
            datetime_end=datetime.now() + timedelta(days=5),
        )
    draft = False
