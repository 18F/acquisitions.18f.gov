from rest_framework import serializers
from projects.models import IAA, Project, AgileBPA, Micropurchase


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
    iaa = IAASerializer()

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'project_type',
            'description',
            'public',
            'iaa',
        )


class AgileBPASerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = AgileBPA
        fields = (
            'id',
            'name',
            'description',
            'public',
            'project',
            'procurement_method',
            'status',
            'set_aside_status',
            'rfq_id',
            'period_of_performance',
            'github_repository',
        )


class MicropurchaseSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Micropurchase
        fields = (
            'id',
            'name',
            'description',
            'public',
            'project',
            'procurement_method',
            'status',
        )
