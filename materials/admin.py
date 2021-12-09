from django.contrib import admin
from materials.models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass