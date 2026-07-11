from django.contrib import admin
from django.db import models
from django.forms import TimeInput
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import ConsultationTime, FreeAdmission, PracticeClosure


class TimeInputWidget(TimeInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"].update({
            "type": "time",
            "step": "900",
            "class": "vTimeField",
        })
        super().__init__(*args, **kwargs)


@admin.register(FreeAdmission)
class FreeAdmissionAdmin(admin.ModelAdmin):
    list_display = ("wochentag_badge", "startzeit", "endzeit", "zeitraum_display")
    list_filter = ("wochentag",)
    search_fields = ("wochentag",)
    ordering = ("wochentag", "startzeit")

    formfield_overrides = {
        models.TimeField: {"widget": TimeInputWidget},
    }

    fieldsets = (
        (
            "📅 Freie Annahme",
            {
                "fields": ("wochentag", ("startzeit", "endzeit")),
                "description": _(
                    "Tragen Sie den Wochentag und die Annahmezeiten ohne Termin ein. "
                    "Zeiten in 15-Minuten-Schritten (z. B. 08:00 – 08:30)."
                ),
            },
        ),
    )

    def wochentag_badge(self, obj):
        color_map = {
            "Mo": "#0d1b3e", "Di": "#1e3a8a", "Mi": "#0a9396",
            "Do": "#065f46", "Fr": "#7c3aed",
        }
        color = color_map.get(obj.wochentag, "#64748b")
        return format_html(
            '<span style="background:{}22; color:{}; padding:3px 12px; '
            'border-radius:12px; font-weight:600; font-size:0.85rem;">{}</span>',
            color, color, obj.get_wochentag_display(),
        )
    wochentag_badge.short_description = _("Wochentag")
    wochentag_badge.admin_order_field = "wochentag"

    def zeitraum_display(self, obj):
        return format_html(
            '<span style="color:#0d1b3e; font-weight:500;">{} – {} Uhr</span>',
            obj.startzeit.strftime("%H:%M"),
            obj.endzeit.strftime("%H:%M"),
        )
    zeitraum_display.short_description = _("Zeitraum")


@admin.register(ConsultationTime)
class ConsultationTimeAdmin(admin.ModelAdmin):
    list_display = (
        "wochentag_badge",
        "startzeit",
        "endzeit",
        "zeitraum_display",
        "nach_vereinbarung",   # raw field needed for list_editable
        "vereinbarung_badge",
    )
    list_filter = ("wochentag", "nach_vereinbarung")
    search_fields = ("wochentag",)
    ordering = ("wochentag", "startzeit")
    list_editable = ("nach_vereinbarung",)

    formfield_overrides = {
        models.TimeField: {"widget": TimeInputWidget},
    }

    fieldsets = (
        (
            "🕐 Sprechzeit",
            {
                "fields": ("wochentag", ("startzeit", "endzeit")),
                "description": _(
                    "Tragen Sie den Wochentag und die regulären Sprechzeiten ein. "
                    "Zeiten in 15-Minuten-Schritten (z. B. 08:00 – 12:00)."
                ),
            },
        ),
        (
            "⚙️ Besondere Bedingungen",
            {
                "fields": ("nach_vereinbarung",),
                "description": _(
                    "Aktivieren Sie diese Option, wenn dieser Zeitraum nur nach "
                    "vorheriger Vereinbarung stattfindet."
                ),
            },
        ),
    )

    def wochentag_badge(self, obj):
        color_map = {
            "Mo": "#0d1b3e", "Di": "#1e3a8a", "Mi": "#0a9396",
            "Do": "#065f46", "Fr": "#7c3aed",
        }
        color = color_map.get(obj.wochentag, "#64748b")
        return format_html(
            '<span style="background:{}22; color:{}; padding:3px 12px; '
            'border-radius:12px; font-weight:600; font-size:0.85rem;">{}</span>',
            color, color, obj.get_wochentag_display(),
        )
    wochentag_badge.short_description = _("Wochentag")
    wochentag_badge.admin_order_field = "wochentag"

    def zeitraum_display(self, obj):
        return format_html(
            '<span style="color:#0d1b3e; font-weight:500;">{} – {} Uhr</span>',
            obj.startzeit.strftime("%H:%M"),
            obj.endzeit.strftime("%H:%M"),
        )
    zeitraum_display.short_description = _("Zeitraum")

    def vereinbarung_badge(self, obj):
        if obj.nach_vereinbarung:
            return format_html(
                '<span style="background:#fef3c7; color:#92400e; padding:2px 10px; '
                'border-radius:10px; font-size:0.78rem; font-weight:600;">Nach Vereinbarung</span>'
            )
        return format_html(
            '<span style="background:#d1fae5; color:#065f46; padding:2px 10px; '
            'border-radius:10px; font-size:0.78rem; font-weight:600;">Regulär</span>'
        )
    vereinbarung_badge.short_description = _("Art")
    # Allow sorting/clicking in list_editable context
    vereinbarung_badge.admin_order_field = "nach_vereinbarung"


@admin.register(PracticeClosure)
class PracticeClosureAdmin(admin.ModelAdmin):
    list_display = ("zeitraum_display", "start_datum", "end_datum", "dauer_display")
    list_filter = ("start_datum",)
    date_hierarchy = "start_datum"
    ordering = ("start_datum",)

    fieldsets = (
        (
            "📅 Praxisschließzeit",
            {
                "fields": (("start_datum", "end_datum"),),
                "description": _(
                    "Tragen Sie den Beginn und das Ende der Schließzeit ein. "
                    "Beide Daten sind einschließlich (inkl.)."
                ),
            },
        ),
    )

    def zeitraum_display(self, obj):
        return format_html(
            '<span style="font-weight:600; color:#0d1b3e;">{} – {}</span>',
            obj.start_datum.strftime("%d.%m.%Y"),
            obj.end_datum.strftime("%d.%m.%Y"),
        )
    zeitraum_display.short_description = _("Schließzeit")
    zeitraum_display.admin_order_field = "start_datum"

    def dauer_display(self, obj):
        delta = (obj.end_datum - obj.start_datum).days + 1
        color = "#065f46" if delta <= 7 else "#92400e" if delta <= 21 else "#7c3aed"
        bg = "#d1fae5" if delta <= 7 else "#fef3c7" if delta <= 21 else "#ede9fe"
        return format_html(
            '<span style="background:{}; color:{}; padding:3px 10px; '
            'border-radius:12px; font-size:0.82rem; font-weight:600;">{} Tag(e)</span>',
            bg, color, delta,
        )
    dauer_display.short_description = _("Dauer")
