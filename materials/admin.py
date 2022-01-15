from django.contrib import admin
from materials.models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    """
    Registers the grade model so it's available for editing on django admin.
    """
