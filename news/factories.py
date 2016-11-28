import factory
from datetime import datetime, timedelta, tzinfo
from dateutil.tz import tzlocal
from django.contrib.auth.models import User
from news.models import Post


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('safe_email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False
    is_superuser = False


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
