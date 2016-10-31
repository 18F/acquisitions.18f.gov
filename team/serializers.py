from rest_framework import serializers
from team.models import Teammate, Role


class TeammateSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.CharField(source='role.name')

    class Meta:
        model = Teammate
        fields = (
            'name',
            'role',
            )


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ('title',)
