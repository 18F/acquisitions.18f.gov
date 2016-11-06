import factory
from team.models import Teammate, Role
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('safe_email')
    is_active = True
    is_staff = False
    is_superuser = False


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
    read_only = factory.Faker('boolean')
    role = factory.SubFactory(RoleFactory)
