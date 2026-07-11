from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from taggit.models import Tag

from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("photo_thumb", "full_name_display", "specialty", "tag_list", "updated")
    list_display_links = ("photo_thumb", "full_name_display")
    search_fields = ("name", "title", "specialty")
    ordering = ("name",)
    readonly_fields = ("photo_preview",)

    fieldsets = (
        (
            "👤 Person",
            {
                "fields": ("photo_preview", "picture", ("title", "name")),
            },
        ),
        (
            "🩺 Fachgebiet & Qualifikationen",
            {
                "fields": ("specialty", "tags"),
            },
        ),
    )

    def photo_thumb(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" style="width:40px; height:40px; border-radius:50%; '
                'object-fit:cover; border:2px solid #e2e8f0;" />',
                obj.picture.url,
            )
        return format_html(
            '<div style="width:40px; height:40px; border-radius:50%; background:#e2e8f0; '
            'display:flex; align-items:center; justify-content:center; color:#94a3b8; font-size:1.2rem;">👤</div>'
        )
    photo_thumb.short_description = ""

    def photo_preview(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" style="width:120px; height:120px; border-radius:12px; '
                'object-fit:cover; border:2px solid #e2e8f0; margin-bottom:8px;" />',
                obj.picture.url,
            )
        return format_html('<span style="color:#94a3b8;">Kein Bild hochgeladen</span>')
    photo_preview.short_description = _("Vorschau")

    def full_name_display(self, obj):
        return format_html(
            '<span style="font-weight:600; color:#0d1b3e;">{} {}</span>',
            obj.title or "",
            obj.name,
        )
    full_name_display.short_description = _("Name")
    full_name_display.admin_order_field = "name"

    def tag_list(self, obj):
        tags = obj.tags.all()
        if not tags:
            return format_html('<span style="color:#94a3b8;">—</span>')
        badges = "".join(
            f'<span style="background:#e0f7f8; color:#0a7378; padding:2px 8px; '
            f'border-radius:10px; font-size:0.75rem; margin-right:4px;">{t.name}</span>'
            for t in tags
        )
        return format_html(badges)
    tag_list.short_description = _("Qualifikationen")


admin.site.unregister(Tag)
