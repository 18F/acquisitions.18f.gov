from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client
from django.shortcuts import reverse
from projects.models import Buy, Project
from projects.factories import BuyFactory
from acquisitions.factories import UserFactory


class TestPrivateBuys(TestCase):
    def setUp(self):
        self.buy = BuyFactory.create(public=False)
        self.user = UserFactory.create()
        self.client = Client()

    def test_with_permission(self):
        content_type = ContentType.objects.get_for_model(Project)
        permission = Permission.objects.get(
            codename='view_project',
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)
        self.client.force_login(self.user)
        print(reverse('buys:buy', args=[self.buy.id]))
        response = self.client.get(reverse('buys:buy', args=[self.buy.id]))
        self.assertTemplateUsed(response, 'projects/buy.html')

    def test_without_permission(self):
        response = self.client.get(reverse('buys:buy', args=[self.buy.id]))
        self.assertTemplateUsed(response, 'projects/private-page.html')
