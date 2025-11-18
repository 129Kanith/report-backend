
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
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "role",
            "department",
            "department_id",
        ]
        read_only_fields = ["role"]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# =========================
#  REPORT SERIALIZER
# =========================
class ReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    attachment = serializers.FileField(required=False)
    date = serializers.SerializerMethodField()

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

    def get_date(self, obj):
        # Convert datetime to date safely
        return obj.date.date() if hasattr(obj.date, 'date') else obj.date


# =========================
#  COMMENT SERIALIZER
# =========================
class CommentSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "admin", "report", "text", "created_at"]
        read_only_fields = ["id", "admin", "created_at"]


