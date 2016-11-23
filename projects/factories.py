import factory
import string
import factory.fuzzy
from projects.models import IAA, Project, Buy, ContractingOffice, \
                            ContractingSpecialist, ContractingOfficer
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
    signed_on = None
    client = factory.Faker('company')


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    iaa = factory.SubFactory(
        IAAFactory,
        signed_on=factory.Faker(
                        'date_time_this_month',
                        before_now=True,
                        after_now=False,
                        tzinfo=None
                    )
    )
    description = factory.Faker('paragraph')
    name = factory.Faker('catch_phrase')
    public = factory.Faker('boolean')


class ContractingOfficeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContractingOffice

    name = factory.Faker('company')
    program_manager = factory.SubFactory(
        UserFactory
    )


class ContractingOfficerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContractingOfficer

    user = factory.SubFactory(
        UserFactory
    )
    office = factory.SubFactory(
        ContractingOfficeFactory
    )


class ContractingSpecialistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContractingSpecialist

    user = factory.SubFactory(
        UserFactory
    )
    office = factory.SubFactory(
        ContractingOfficeFactory
    )


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


class AddBuyFactory(BuyFactory):
    project = factory.Iterator(Project.objects.all())
