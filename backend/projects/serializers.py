from rest_framework import serializers
from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    start = serializers.DateField()
    end = serializers.DateField()
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'start', 'end')

