from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# =========================
#  DEPARTMENT MODEL
# =========================
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# =========================
#  CUSTOM USER MODEL
# =========================
class User(AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("EMPLOYEE", "Employee"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="EMPLOYEE")
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


# =========================
#  REPORT MODEL
# =========================
class Report(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reports"
    )
    date = models.DateField(default=timezone.now)
    work_description = models.TextField()
    hours_spent = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    attachment = models.FileField(upload_to="attachments/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.status}"


# =========================
#  COMMENT MODEL
# =========================
class Comment(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name="comments"
    )
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"role": "ADMIN"}
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.admin.username} on {self.report}"


