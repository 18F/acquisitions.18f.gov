import pytest
from projects.factories import (
    IAAFactory,
)


class TestIAAModel:
    @pytest.mark.django_db
    def test_budget(self):
        iaa = IAAFactory.create(
            cogs_amount=75,
            non_cogs_amount=25,
        )
        assert iaa.budget() == 100
