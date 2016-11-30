import factory
from team.models import Teammate, Role
from acquisitions.factories import UserFactory


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    name = factory.Faker('job')


class TeammateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teammate

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('name')
    bio = factory.Faker('paragraphs')
    github = factory.Faker('user_name')
    slack = factory.Faker('user_name')
    role = factory.SubFactory(RoleFactory)
