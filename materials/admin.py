from django.contrib import admin
from materials.models import Grade, Topic, Note, Tip


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

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    Registers the grade model so it's available for editing on django admin.
    """


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    """
    Registers the grade model so it's available for editing on django admin.
    """
