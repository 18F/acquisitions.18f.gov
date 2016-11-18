from rest_framework import serializers
from projects.models import IAA, Project, Buy


class IAASerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IAA
        fields = (
            'id',
            'client',
        )


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'name',
            'project_type',
            'description',
        )


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = (
            'name',
            'description',
        )
