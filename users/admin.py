from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, Team, Enrollment


@register(Enrollment)
class EnrollmentAdmin(ModelAdmin):
    model = Enrollment


@register(Profile)
class ProfileAdmin(ModelAdmin):
    model = Profile


@register(Team)
class TeamAdmin(ModelAdmin):
    model = Team
