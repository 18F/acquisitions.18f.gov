from rest_framework import serializers
from team.models import Teammate, Role


class TeammateSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.CharField(source='role.name')

    class Meta:
        model = Teammate
        fields = (
            'name',
            'role',
            'photo',
            )


class TeammatePlusSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.CharField(source='role.name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Teammate
        fields = (
            'name',
            'role',
            'photo',
            'github',
            'slack',
            'email',
            )


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ('name',)
