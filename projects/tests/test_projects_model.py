import pytest
from projects.factories import IAAFactory, ProjectFactory, BuyFactory


class TestProjectsModel:
    @pytest.mark.django_db
    def test_budget_remaining(self):
        project = ProjectFactory.create(dollars=200)
        buy = BuyFactory.create(dollars=50, project=project)
        assert project.budget_remaining() == 150
        buy2 = BuyFactory.create(dollars=50, project=project)
        assert project.budget_remaining() == 100

    @pytest.mark.django_db
    def test_budget_remaining_clean(self):
        project = ProjectFactory.create(dollars=200)
        buy = BuyFactory.create(
            dollars=150,
            project=project,
            public=project.public
        )
        buy.full_clean()
