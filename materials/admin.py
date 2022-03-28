from django.contrib import admin
from materials.models import Grade, Topic


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    """
    Registers the grade model so it's available for editing on django admin.
    """


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """
    Registers the grade model so it's available for editing on django admin.
    """
