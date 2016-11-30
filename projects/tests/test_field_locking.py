import pytest
from datetime import date
from django.core.exceptions import ValidationError
from projects.models import Buy, Project
from projects.factories import BuyFactory, UserFactory, ProjectFactory, \
                               ContractingOfficeFactory, \
                               ContractingOfficerFactory, \
                               ContractingSpecialistFactory


@pytest.mark.django_db
def test_cannot_issue():
    project = ProjectFactory(public=True)
    buy = BuyFactory(project=project)
    assert not buy.ready_to_issue()
    with pytest.raises(ValidationError):
        buy.issue_date = date.today()
        buy.full_clean()
        buy.save()


@pytest.mark.django_db
def test_can_issue():
    project = ProjectFactory(public=True)
    buy = BuyFactory(project=project)
    buy.contracting_office = ContractingOfficeFactory()
    buy.contracting_officer = ContractingOfficerFactory()
    buy.contracting_specialist = ContractingSpecialistFactory()
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
    assert buy.ready_to_issue()
    buy.issue_date = date.today()
    buy.full_clean()
    buy.save()
    assert buy.issue_date == date.today()


@pytest.mark.django_db
def test_locked_after_issuance():
    project = ProjectFactory(public=True)
    buy = BuyFactory(project=project)
    buy.issue_date = date.today()
    buy.save()
    with pytest.raises(ValidationError):
        buy.dollars = 1
        buy.full_clean()
        buy.save()


@pytest.mark.django_db
def test_can_award():
    project = ProjectFactory(public=True)
    buy = BuyFactory(project=project)
    buy.contracting_office = ContractingOfficeFactory()
    buy.contracting_officer = ContractingOfficerFactory()
    buy.contracting_specialist = ContractingSpecialistFactory()
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
    buy.issue_date = date.today()
    buy.award_date = date.today()
    buy.full_clean()
    buy.save()
