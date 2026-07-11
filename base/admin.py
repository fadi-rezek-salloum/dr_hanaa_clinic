from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # ── List View ────────────────────────────────────────────────────────────
    list_display = (
        "colored_name",
        "betreff_short",
        "email",
        "telefon_display",
        "eingangsdatum",
        "uhrzeit",
        "alter_badge",
    )
    list_display_links = ("colored_name",)
    list_filter = ("submitted_at",)
    search_fields = ("vorname", "name", "email", "betreff", "nachricht")
    ordering = ("-submitted_at",)
    date_hierarchy = "submitted_at"
    list_per_page = 25
    show_full_result_count = True

    # ── Detail View ──────────────────────────────────────────────────────────
    readonly_fields = (
        "vorname", "name", "email", "telefon", "betreff", "nachricht",
        "submitted_at_formatted", "alter_badge",
    )

    fieldsets = (
        (
            "📋 Patienteninformationen",
            {
                "fields": (("vorname", "name"), ("email", "telefon")),
            },
        ),
        (
            "✉️ Nachricht",
            {
                "fields": ("betreff", "nachricht"),
            },
        ),
        (
            "🕐 Zeitstempel",
            {
                "fields": ("submitted_at_formatted", "alter_badge"),
                "classes": ("collapse",),
                "description": "Diese Felder werden automatisch gesetzt und können nicht geändert werden.",
            },
        ),
    )

    # ── Custom Display Methods ────────────────────────────────────────────────
    def colored_name(self, obj):
        return format_html(
            '<span style="font-weight:600; color:#0d1b3e;">{} {}</span>',
            obj.vorname,
            obj.name,
        )
    colored_name.short_description = _("Patient")
    colored_name.admin_order_field = "name"

    def betreff_short(self, obj):
        betreff = obj.betreff
        if len(betreff) > 45:
            return format_html(
                '<span title="{}">{}&hellip;</span>',
                betreff,
                betreff[:45],
            )
        return betreff
    betreff_short.short_description = _("Betreff")
    betreff_short.admin_order_field = "betreff"

    def telefon_display(self, obj):
        if obj.telefon:
            return format_html(
                '<a href="tel:{}" style="color:#0a9396;">{}</a>',
                obj.telefon,
                obj.telefon,
            )
        return format_html('<span style="color:#94a3b8;">—</span>')
    telefon_display.short_description = _("Telefon")

    def eingangsdatum(self, obj):
        local = localtime(obj.submitted_at)
        return format_html(
            '<span style="font-weight:500; color:#0d1b3e;">{}</span>',
            local.strftime("%d.%m.%Y"),
        )
    eingangsdatum.short_description = _("Datum")
    eingangsdatum.admin_order_field = "submitted_at"

    def uhrzeit(self, obj):
        local = localtime(obj.submitted_at)
        return format_html(
            '<span style="color:#64748b;">{}</span>',
            local.strftime("%H:%M Uhr"),
        )
    uhrzeit.short_description = _("Uhrzeit")
    uhrzeit.admin_order_field = "submitted_at"

    def alter_badge(self, obj):
        from django.utils import timezone
        import math
        delta = timezone.now() - obj.submitted_at
        hours = delta.total_seconds() / 3600

        if hours < 2:
            color, bg, label = "#065f46", "#d1fae5", f"Vor {int(delta.total_seconds()//60)} Min."
        elif hours < 24:
            color, bg, label = "#92400e", "#fef3c7", f"Vor {int(hours)} Std."
        elif delta.days < 7:
            color, bg, label = "#1e40af", "#dbeafe", f"Vor {delta.days} Tag(en)"
        else:
            color, bg, label = "#64748b", "#f1f5f9", f"Vor {math.ceil(delta.days/7)} Woche(n)"

        return format_html(
            '<span style="background:{bg}; color:{color}; padding:3px 10px; '
            'border-radius:12px; font-size:0.78rem; font-weight:600; white-space:nowrap;">'
            '{label}</span>',
            bg=bg, color=color, label=label,
        )
    alter_badge.short_description = _("Eingang")

    def submitted_at_formatted(self, obj):
        local = localtime(obj.submitted_at)
        return format_html(
            '<strong style="font-size:1rem; color:#0d1b3e;">{}</strong>',
            local.strftime("%A, %d. %B %Y um %H:%M Uhr"),
        )
    submitted_at_formatted.short_description = _("Eingegangen am")

    # Prevent anyone from accidentally adding contacts manually via admin
    def has_add_permission(self, request):
        return False
