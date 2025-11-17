
from rest_framework import serializers

from .models import User, Department, Report, Comment


# =========================
#  DEPARTMENT SERIALIZER
# =========================
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]


# =========================
#  USER SERIALIZER
# =========================
class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source="department", write_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "department",
            "department_id",
        ]
        read_only_fields = ["role"]


# =========================
#  REPORT SERIALIZER
# =========================
class ReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    attachment = serializers.FileField(required=False)

    class Meta:
        model = Report
        fields = [
            "id",
            "user",
            "date",
            "work_description",
            "hours_spent",
            "status",
            "attachment",
        ]
        read_only_fields = ["id", "user", "date"]


# =========================
#  COMMENT SERIALIZER
# =========================
class CommentSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "admin", "report", "text", "created_at"]
        read_only_fields = ["id", "admin", "created_at"]


