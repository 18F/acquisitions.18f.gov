import factory
from projects.models import IAA, Project


class IAAFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IAA

    id = factory.Faker('md5')
    client = factory.Faker('company')


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    iaa = factory.SubFactory(IAAFactory)
    description = factory.Faker('paragraphs')
    name = factory.Faker('catch_phrase')
