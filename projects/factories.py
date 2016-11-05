import factory
import string
import factory.fuzzy
from projects.models import IAA, Project


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
