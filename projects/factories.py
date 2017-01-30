import factory
import string
import factory.fuzzy
import random
from acquisitions.factories import UserFactory
from projects.models import (
    Agency,
    AgencyOffice,
    Buy,
    ContractingOffice,
    ContractingOfficer,
    ContractingOfficerRepresentative,
    ContractingSpecialist,
    IAA,
    ProcurementMethod,
    Project,
)


class AgencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Agency

    # TODO: Create a Faker provider for agency names
    name = factory.Faker('company')
    address = factory.Faker('address')
    business_partner_number = factory.Faker('random_number', digits=9)
    location_code = factory.Faker('random_number', digits=8)


class AgencyOfficeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AgencyOffice

    name = factory.Faker('company')
    agency = factory.SubFactory(
        AgencyFactory
    )
    address = factory.Faker('address')


class IAAFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IAA

    id = factory.fuzzy.FuzzyText(
        prefix='IAA',
        chars=string.digits,
        )
    budget = factory.Faker('random_int', min=5000, max=99999)
    assisted_acquisition = factory.Faker('boolean')
    signed_on = None
    business_event_type_code = factory.Faker(
                                    'password',
                                    length=8,
                                    special_chars=False,
                                    lower_case=False,
                                )
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
    def non_cogs_amount(self):
        min = 1000
        max = self.iaa.budget
        return random.randint(min, max)

    @factory.lazy_attribute
    def cogs_amount(self):
        min = 0
        max = self.iaa.budget - self.non_cogs_amount
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

class ProcurementMethodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProcurementMethod

    name = factory.Faker('color_name')
    short_name = factory.Faker('password')

class BuyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Buy


    project = factory.SubFactory(
        ProjectFactory,
        public=factory.SelfAttribute('..public')
    )
    procurement_method = factory.SubFactory(
        ProcurementMethodFactory
    )
    description = factory.Faker('paragraph')
    name = factory.Faker('catch_phrase')
    public = factory.Faker('boolean')

    @factory.lazy_attribute
    def dollars(self):
        min = 500
        max = self.project.budget()
        return random.randint(min, max)


class AddBuyFactory(BuyFactory):
    project = factory.Iterator(Project.objects.all())
