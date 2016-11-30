import pytest
from datetime import date
from django.core.exceptions import ValidationError
from projects.models import Buy, Project
from projects.factories import BuyFactory


@pytest.mark.django_db
def test_cannot_issue():
    buy = BuyFactory()
    assert not buy.ready_to_issue()
    with pytest.raises(ValidationError):
        buy.issue_date = date.today()
        buy.full_clean()
        buy.save()


@pytest.mark.django_db
def test_can_issue():
    buy = BuyFactory()
    # do a bunch of buy data stuff here
    assert buy.ready_to_issue()
    buy.issue_date = date.today()
    buy.full_clean()
    buy.save()
    assert buy.issue_date == date.today()


@pytest.mark.django_db
def test_locked_after_issuance():
    buy = BuyFactory()
    # do a bunch of buy data stuff here
    buy.issue_date = date.today()
    buy.save()
    with pytest.raises(ValidationError):
        buy.dollars = 1
        buy.full_clean()
        buy.save()


@pytest.mark.django_db
def test_can_award():
    buy = BuyFactory()
    # do a bunch of buy data stuff here
    buy.award_date = date.today()
    buy.full_clean()
    buy.save()
