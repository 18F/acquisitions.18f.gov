from rest_framework import serializers
from projects.models import IAA, Project, Buy


class IAASerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IAA
        fields = (
            'id',
            'client',
        )


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = (
            'name',
            'description',
        )


class ProjectSerializer(serializers.ModelSerializer):
    buys = BuySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            'name',
            'project_type',
            'description',
            'buys',
        )
