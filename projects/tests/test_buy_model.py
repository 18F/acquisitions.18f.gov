import pytest
from django.template.loader import TemplateDoesNotExist
from projects.factories import IAAFactory, ProjectFactory, BuyFactory


class TestBuyModel:
    @pytest.fixture
    @pytest.mark.django_db
    def buy(self):
        buy = BuyFactory()
        return buy

    @pytest.mark.django_db
    def test_is_private(self):
        project = ProjectFactory(public=True)
        buy = BuyFactory(project=project, public=True)
        assert buy.is_private() is False
        buy.public = False
        assert buy.is_private() is True

    @pytest.mark.django_db
    def test_status(self, buy):
        assert buy.status() == "Planning"

    @pytest.mark.django_db
    def test_is_micropurchase(self):
        iaa = IAAFactory(dollars=500000)
        project = ProjectFactory(iaa=iaa, dollars=300000)
        buy = BuyFactory(project=project, dollars=2000)
        assert buy.is_micropurchase() is True
        buy.dollars = 3500
        assert buy.is_micropurchase() is True
        buy.dollars = 3501
        assert buy.is_micropurchase() is False

    @pytest.mark.django_db
    def test_is_under_sat(self):
        iaa = IAAFactory(dollars=500000)
        project = ProjectFactory(iaa=iaa, dollars=300000)
        buy = BuyFactory(project=project, dollars=2000)
        assert buy.is_under_sat() is True
        buy.dollars = 15000
        assert buy.is_under_sat() is True
        buy.dollars = 150000
        assert buy.is_under_sat() is True
        buy.dollars = 150001
        assert buy.is_under_sat() is False

    @pytest.mark.django_db
    def test_create_document(self):
        buy = BuyFactory(procurement_method='agile_bpa')
        assert not buy.qasp
        buy.create_document('qasp')
        assert buy.qasp

    @pytest.mark.django_db
    def test_not_create_document(self):
        buy = BuyFactory(procurement_method='micropurchase')
        with pytest.raises(TemplateDoesNotExist):
            buy.create_document('acquisition_plan')

    @pytest.mark.django_db
    def test_available_documents(self):
        buy = BuyFactory(procurement_method='agile_bpa')
        assert set(buy.available_docs(access_private=True)) == set([
            'qasp',
            'acquisition_plan',
            'pws',
            'rfq',
            'interview_questions',
            'market_research',
        ])
        assert 'acquisition_plan' not in buy.available_docs(access_private=False)

    @pytest.mark.django_db
    def test_document_status(self):
        buy = BuyFactory(procurement_method='agile_bpa')
        assert buy.doc_status('market_research') == "100.00% Complete"
