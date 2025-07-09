from tokenize import Comment
from rest_framework import serializers
from users.models import User
from tasks.models import Task
from .models import Comments


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "project",
            "assigned_to",
            "due_date",
            "created",
        ]


class TaskUpdateSerializer(serializers.ModelSerializer):
    assign_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )

    class Meta:
        model = Task
        fields = "__all__"

    def update(self, instance, validated_data):
        assign_to = validated_data.pop("assign_to", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if assign_to is not None:
            instance.assign_to.set(assign_to)

        return instance


class TaskCreateSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "priority",
            "project",
            "assigned_to",
            "due_date",
        ]


class TaskAssignUserSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Task
        fields = ["assigned_to"]


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comments
        fields = ["id", "task", "author", "author_name", "content", "created_at"]
