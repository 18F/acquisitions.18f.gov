import factory
import string
import factory.fuzzy
from projects.models import IAA, Project, Buy
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('safe_email')
    is_active = True
    is_staff = False
    is_superuser = False


class IAAFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IAA

    id = factory.fuzzy.FuzzyText(
        prefix='IAA',
        chars=string.digits,
        )
    client = factory.Faker('company')


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    iaa = factory.SubFactory(IAAFactory)
    description = factory.Faker('paragraph')
    name = factory.Faker('catch_phrase')
    public = factory.Faker('boolean')


class BuyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Buy

    project = factory.SubFactory(
        ProjectFactory,
        public=factory.SelfAttribute('..public')
    )
    description = factory.Faker('paragraph')
    name = factory.Faker('catch_phrase')
    public = factory.Faker('boolean')
