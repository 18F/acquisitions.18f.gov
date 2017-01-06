import pytest
from datetime import date
from django.core.exceptions import ValidationError
from projects.models import Buy, Project
from projects.factories import (
    BuyFactory,
    ProjectFactory,
    ContractingOfficeFactory,
    ContractingOfficerFactory,
    ContractingSpecialistFactory,
    ContractingOfficerRepresentativeFactory
)
from acquisitions.factories import UserFactory


class TestLocking:
    @pytest.fixture
    @pytest.mark.django_db
    def buy(self):
        project = ProjectFactory(public=True)
        buy = BuyFactory(project=project)
        return buy

    @pytest.fixture
    @pytest.mark.django_db
    def buy_plus(self, buy):
        buy.acquisition_plan = '# ACQ PLAN'
        buy.base_period_length = '3 months'
        buy.competition_strategy = 'Set-Aside'
        buy.contract_type = 'Time and Materials'
        buy.contracting_office = ContractingOfficeFactory()
        buy.contracting_officer = ContractingOfficerFactory()
        buy.contracting_officer_representative = ContractingOfficerRepresentativeFactory()
        buy.contracting_specialist = ContractingSpecialistFactory()
        buy.dollars = 12
        buy.github_repository = 'https://github.com/18f/wow_such_repo/'
        buy.naics_code = 444444
        buy.option_period_length = '3 months'
        buy.option_periods = 3
        buy.procurement_method = 'agile_bpa'
        buy.product_owner = UserFactory()
        buy.public = True
        buy.qasp = '# QASP'
        buy.rfq_id = 'abc12345678'
        buy.set_aside_status = 'Small Business'
        return buy

    @pytest.mark.django_db
    def test_cannot_issue(self, buy):
        assert not buy.ready_to_issue()
        with pytest.raises(ValidationError):
            buy.issue_date = date.today()
            print(buy.delivery_date)
            buy.full_clean()
            buy.save()


    @pytest.mark.django_db
    def test_can_issue(self, buy_plus):
        assert buy_plus.ready_to_issue()
        buy_plus.issue_date = date.today()
        buy_plus.full_clean()
        buy_plus.save()
        assert buy_plus.issue_date == date.today()


    @pytest.mark.django_db
    def test_locked_after_issuance(self, buy):
        buy.issue_date = date.today()
        buy.save()
        with pytest.raises(ValidationError):
            buy.dollars = 1
            buy.full_clean()
            buy.save()


    @pytest.mark.django_db
    def test_can_award(self, buy_plus):
        buy_plus.issue_date = date.today()
        buy_plus.award_date = date.today()
        buy_plus.full_clean()
        buy_plus.save()
