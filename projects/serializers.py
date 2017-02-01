from rest_framework import serializers
from projects.models import Agency, AgencyOffice, IAA, Project, Buy


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = (
            'name',
            'address',
        )


class ClientSerializer(serializers.ModelSerializer):
    agency = AgencySerializer()
    client = serializers.CharField(
        source='__str__'
    )

    class Meta:
        model = AgencyOffice
        fields = (
            'id',
            'client',
            'agency',
        )


class IAASerializer(serializers.ModelSerializer):
    client = ClientSerializer()

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
    set_aside_status = serializers.CharField(
        source='get_set_aside_status_display'
    )

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
            'period_of_performance',
        )
