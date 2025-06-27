from django.contrib import admin
from django.utils.html import format_html
from .models import Meeting, AgendaItem, Attachment

class AgendaItemInline(admin.TabularInline):
    model = AgendaItem
    extra = 0

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0
    readonly_fields = ('display_file_name', 'uploaded_at')
    fields = ('display_file_name', 'file_type', 'uploaded_at')

    def display_file_name(self, obj):
        if obj.file:
            return format_html('<a href="{}">{}</a>', obj.file.url, obj.file.name)
        return "-"
    display_file_name.short_description = 'File'

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'start_time', 'end_time', 'location', 'attendees', 'minutes')
    list_filter = ('date', 'location')
    search_fields = ('title', 'attendees', 'minutes')
    inlines = [AgendaItemInline, AttachmentInline]

@admin.register(AgendaItem)
class AgendaItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'meeting', 'item_number', 'item_title', 'responsible_person', 'estimated_time')
    list_filter = ('meeting__date', 'responsible_person')
    search_fields = ('item_title', 'description', 'responsible_person')

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'meeting', 'display_file_name', 'uploaded_at')
    list_filter = ('meeting__date', 'uploaded_at')
    search_fields = ('file',)

    def display_file_name(self, obj):
        return format_html('<a href="{}">{}</a>', obj.file.url, obj.file.name)
    display_file_name.short_description = 'File'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('meeting')