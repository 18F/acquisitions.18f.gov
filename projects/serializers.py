from rest_framework import serializers
from projects.models import IAA, Project


class IaaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IAA
        fields = (
            'id',
            'client',
            )


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = (
            'name',
            'project_type',
            'description'
            )
