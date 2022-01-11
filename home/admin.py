from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    Registers the Announcement model so it's available for editing on django admin.
    """
