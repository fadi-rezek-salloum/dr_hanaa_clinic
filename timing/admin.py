from django.contrib import admin
from django.db import models
from django.forms import TimeInput
from django.utils.translation import gettext_lazy as _

from .models import ConsultationTime, FreeAdmission, PracticeClosure


class FreeAdmissionAdmin(admin.ModelAdmin):
    list_display = ("wochentag", "startzeit", "endzeit", "display_full_time_range")
    list_filter = ("wochentag",)
    search_fields = ("wochentag",)
    ordering = ("wochentag", "startzeit")
    date_hierarchy = None

    formfield_overrides = {
        models.TimeField: {
            "widget": TimeInput(
                attrs={
                    "type": "time",
                    "step": "900",
                    "class": "vTimeField",
                    "placeholder": "HH:MM (z.B. 08:00)",
                }
            ),
        },
    }

    def display_full_time_range(self, obj):
        return f"{obj.startzeit.strftime('%H:%M')} - {obj.endzeit.strftime('%H:%M')} Uhr"

    display_full_time_range.short_description = _("Zeitraum")

    fieldsets = (
        (_("Allgemeine Informationen"), {"fields": ("wochentag",)}),
        (
            _("Zeitliche Angaben"),
            {
                "fields": ("startzeit", "endzeit"),
                "description": _(
                    "Wählen Sie die Start- und Endzeit in 15-Minuten-Schritten. Beispiel: 08:00 - 08:30."
                ),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["startzeit"].help_text = _(
            "Startzeit in 24-Stunden-Format (z.B. 08:00)."
        )
        form.base_fields["endzeit"].help_text = _("Endzeit in 24-Stunden-Format (z.B. 08:30).")
        return form


class ConsultationTimeAdmin(admin.ModelAdmin):
    list_display = (
        "wochentag",
        "startzeit",
        "endzeit",
        "nach_vereinbarung",
        "display_full_time_range",
    )
    list_filter = ("wochentag", "nach_vereinbarung")
    search_fields = ("wochentag",)
    ordering = ("wochentag", "startzeit")
    list_editable = ("nach_vereinbarung",)

    formfield_overrides = {
        models.TimeField: {
            "widget": TimeInput(
                attrs={
                    "type": "time",
                    "step": "900",
                    "class": "vTimeField",
                    "placeholder": "HH:MM (z.B. 14:00)",
                }
            ),
        },
    }

    def display_full_time_range(self, obj):
        return f"{obj.startzeit.strftime('%H:%M')} - {obj.endzeit.strftime('%H:%M')} Uhr {'(nach Vereinbarung)' if obj.nach_vereinbarung else ''}"

    display_full_time_range.short_description = _("Zeitraum")

    fieldsets = (
        (_("Allgemeine Informationen"), {"fields": ("wochentag",)}),
        (
            _("Zeitliche Angaben"),
            {
                "fields": ("startzeit", "endzeit"),
                "description": _(
                    "Wählen Sie die Start- und Endzeit in 15-Minuten-Schritten. Beispiel: 14:00 - 16:00."
                ),
            },
        ),
        (
            _("Besondere Bedingungen"),
            {
                "fields": ("nach_vereinbarung",),
                "description": _("Aktivieren Sie, wenn die Sprechzeit nach Vereinbarung ist."),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["startzeit"].help_text = _(
            "Startzeit in 24-Stunden-Format (z.B. 14:00)."
        )
        form.base_fields["endzeit"].help_text = _("Endzeit in 24-Stunden-Format (z.B. 16:00).")
        return form


@admin.register(PracticeClosure)
class PracticeClosureAdmin(admin.ModelAdmin):
    list_display = ("start_datum", "end_datum", "duration_days")
    list_filter = ("start_datum", "end_datum")
    date_hierarchy = "start_datum"
    ordering = ("start_datum",)

    def duration_days(self, obj):
        delta = (obj.end_datum - obj.start_datum).days + 1
        return f"{delta} Tag(e)"

    duration_days.short_description = _("Dauer")

    fieldsets = (
        (
            _("Zeitraum"),
            {
                "fields": ("start_datum", "end_datum"),
                "description": _("Wählen Sie den Start- und Enddatum der Schließzeit."),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["start_datum"].help_text = _(
            "Startdatum der Schließzeit (z.B. 08.08.2025)."
        )
        form.base_fields["end_datum"].help_text = _(
            "Enddatum der Schließzeit (z.B. 31.08.2025)."
        )
        return form


admin.site.register(FreeAdmission, FreeAdmissionAdmin)
admin.site.register(ConsultationTime, ConsultationTimeAdmin)
