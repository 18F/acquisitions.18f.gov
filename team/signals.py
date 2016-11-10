from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from team.models import Teammate


@receiver(post_save, sender=Teammate)
def add_to_teammate_group(sender, instance, created, **kwargs):
    try:
        group = Group.objects.get(name='Teammates')
    except Group.DoesNotExist:
        print('Teammates group not yet created')
        return
    if created:
        instance.user.groups.add(group)
