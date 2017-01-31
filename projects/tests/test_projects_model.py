import pytest
from projects.factories import IAAFactory, ProjectFactory, BuyFactory


class TestProjectsModel:
    @pytest.mark.django_db
    def test_budget(self):
        project = ProjectFactory.create(
            cogs_amount=75,
            non_cogs_amount=25,
        )
        assert project.budget() == 100

    @pytest.mark.django_db
    def test_budget_remaining(self):
        project = ProjectFactory.create(non_cogs_amount=200, cogs_amount=0)
        buy = BuyFactory.create(budget=50, project=project)
        assert project.budget_remaining() == 150
        buy2 = BuyFactory.create(budget=50, project=project)
        assert project.budget_remaining() == 100

    @pytest.mark.django_db
    def test_budget_remaining_clean(self):
        project = ProjectFactory.create(non_cogs_amount=200)
        buy = BuyFactory.create(
            budget=150,
            project=project,
            public=project.public
        )
        buy.full_clean()
