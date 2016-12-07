import factory
import string
import factory.fuzzy
import random
from acquisitions.factories import UserFactory
from projects.models import IAA, Project, AgileBPA, ContractingOffice, \
                            ContractingSpecialist, ContractingOfficer, \
                            ContractingOfficerRepresentative, Agency, \
                            AgencyOffice


class AgencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Agency

    # TODO: Create a Faker provider for agency names
    name = factory.Faker('company')


class AgencyOfficeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AgencyOffice

    name = factory.Faker('company')
    agency = factory.SubFactory(
        AgencyFactory
    )


class IAAFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IAA

    id = factory.fuzzy.FuzzyText(
        prefix='IAA',
        chars=string.digits,
        )
    dollars = factory.fuzzy.FuzzyInteger(1000, 999999)
    signed_on = None
    client = factory.SubFactory(AgencyOfficeFactory)


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

    @factory.lazy_attribute
    def dollars(self):
        min = 1000
        max = self.iaa.dollars
        return random.randint(min, max)


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


class ContractingOfficerRepresentativeFactory(
    factory.django.DjangoModelFactory
):
    class Meta:
        model = ContractingOfficerRepresentative

    user = factory.SubFactory(
        UserFactory
    )
    office = factory.SubFactory(
        ContractingOfficeFactory
    )


class AgileBPAFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AgileBPA

    project = factory.SubFactory(
        ProjectFactory,
        public=factory.SelfAttribute('..public')
    )
    description = factory.Faker('paragraph')
    name = factory.Faker('catch_phrase')
    public = factory.Faker('boolean')

    @factory.lazy_attribute
    def dollars(self):
        min = 500
        max = self.project.dollars
        return random.randint(min, max)


class AddAgileBPAFactory(AgileBPAFactory):
    project = factory.Iterator(Project.objects.all())
