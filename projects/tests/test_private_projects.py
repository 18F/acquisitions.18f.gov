from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client
from django.shortcuts import reverse
from projects.models import Buy, Project
from projects.factories import BuyFactory, ProjectFactory
from acquisitions.factories import UserFactory


class TestPrivateProjects(TestCase):
    def setUp(self):
        self.project = ProjectFactory.create(public=False)
        self.user = UserFactory.create()
        self.client = Client()

    def test_with_permission(self):
        content_type = ContentType.objects.get_for_model(Project)
        permission = Permission.objects.get(
            codename='view_private',
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)
        self.client.force_login(self.user)
        response = self.client.get(reverse('projects:project', args=[self.project.id]))
        self.assertTemplateUsed(response, 'projects/project.html')

    def test_without_permission(self):
        response = self.client.get(reverse('projects:project', args=[self.project.id]))
        self.assertTemplateUsed(response, 'projects/private-page.html')
