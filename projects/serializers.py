from rest_framework import serializers
from projects.models import IAA, Project, Buy


class IAASerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = IAA
        fields = (
            'id',
            'client',
            'signed_on',
        )


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'project_type',
            'description',
            'public',
        )


class BuySerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Buy
        fields = (
            'id',
            'name',
            'description',
            'public',
            'project',
            'procurement_method',
            'set_aside_status',
            'period_of_performance',
        )
