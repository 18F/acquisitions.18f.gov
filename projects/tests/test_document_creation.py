import pytest
from datetime import date
from django.template import TemplateDoesNotExist
from projects.factories import (
    BuyFactory,
)
from acquisitions.factories import UserFactory


@pytest.mark.django_db
def test_create_buy_document():
    buy = BuyFactory(procurement_method='agile_bpa')
    assert not buy.qasp
    buy.create_document('qasp')
    assert buy.qasp
