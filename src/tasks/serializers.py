from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class meta:
        model = Tasks
        field = "__all__"
