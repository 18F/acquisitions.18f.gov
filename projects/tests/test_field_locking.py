import pytest
from datetime import date
from django.core.exceptions import ValidationError
from projects.models import AgileBPA, Project
from projects.factories import AgileBPAFactory, ProjectFactory, \
                               ContractingOfficeFactory, \
                               ContractingOfficerFactory, \
                               ContractingSpecialistFactory, \
                               ContractingOfficerRepresentativeFactory


class TestLocking:
    @pytest.fixture
    @pytest.mark.django_db
    def buy(self):
        project = ProjectFactory(public=True)
        buy = AgileBPAFactory(project=project)
        return buy

    @pytest.fixture
    @pytest.mark.django_db
    def buy_plus(self, buy):
        buy.contracting_office = ContractingOfficeFactory()
        buy.contracting_officer = ContractingOfficerFactory()
        buy.contracting_specialist = ContractingSpecialistFactory()
        buy.contracting_officer_representative = ContractingOfficerRepresentativeFactory()
        buy.base_period_length = '3 months'
        buy.option_periods = 3
        buy.option_period_length = '3 months'
        buy.dollars = 1234
        buy.public = True
        buy.rfq_id = 'abc12345678'
        buy.procurement_method = 'Agile BPA'
        buy.set_aside_status = 'Small Business'
        buy.github_repository = 'https://github.com/18f/wow_such_repo/'
        buy.qasp = '# QASP'
        buy.acquisition_plan = '# ACQ PLAN'
        return buy

    @pytest.mark.django_db
    def test_cannot_issue(self, buy):
        assert not buy.ready_to_issue()
        with pytest.raises(ValidationError):
            buy.issue_date = date.today()
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
