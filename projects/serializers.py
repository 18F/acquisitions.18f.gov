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


class BuySerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    procurement_method = serializers.CharField(source='get_procurement_method_display')
    set_aside_status = serializers.CharField(source='get_set_aside_status_display')

    class Meta:
        model = Buy
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
