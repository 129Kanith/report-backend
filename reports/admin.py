from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Department, Report, Comment


# =========================
#  DEPARTMENT ADMIN
# =========================
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


# =========================
#  CUSTOM USER ADMIN
# =========================
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Additional Info",
            {
                "fields": ("role", "department"),
            },
        ),
    )
    list_display = ("id", "username", "email", "role", "department", "is_staff")
    list_filter = ("role", "department")
    search_fields = ("username", "email")
    ordering = ("username",)


admin.site.register(User, UserAdmin)


# =========================
#  REPORT ADMIN
# =========================
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "status", "hours_spent")
    list_filter = ("status", "date", "user__department")
    search_fields = ("user__username", "work_description")
    ordering = ("-date",)
    readonly_fields = ("date",)


# =========================
#  COMMENT ADMIN
# =========================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "admin", "created_at")
    list_filter = ("admin", "created_at")
    search_fields = ("report__user__username", "text")
    ordering = ("-created_at",)
