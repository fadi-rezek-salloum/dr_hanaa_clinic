from django.db import models
from django.utils.translation import gettext_lazy as _


class FreeAdmission(models.Model):
    TAG_WAHLAUSWAHL = [
        ("Mo", _("Montag")),
        ("Di", _("Dienstag")),
        ("Mi", _("Mittwoch")),
        ("Do", _("Donnerstag")),
        ("Fr", _("Freitag")),
    ]

    wochentag = models.CharField(
        max_length=10, choices=TAG_WAHLAUSWAHL, default="Mo", verbose_name=_("Wochentag")
    )
    startzeit = models.TimeField(verbose_name=_("Startzeit"))
    endzeit = models.TimeField(verbose_name=_("Endzeit"))

    def __str__(self):
        return f"{self.get_wochentag_display()} {self.startzeit} - {self.endzeit}"

    class Meta:
        verbose_name = _("Freie Annahme")
        verbose_name_plural = _("Freie Annahmen")


class ConsultationTime(models.Model):
    TAG_WAHLAUSWAHL = [
        ("Mo", _("Montag")),
        ("Di", _("Dienstag")),
        ("Mi", _("Mittwoch")),
        ("Do", _("Donnerstag")),
        ("Fr", _("Freitag")),
    ]

    wochentag = models.CharField(
        max_length=10, choices=TAG_WAHLAUSWAHL, default="Mo", verbose_name=_("Wochentag")
    )
    startzeit = models.TimeField(verbose_name=_("Startzeit"))
    endzeit = models.TimeField(verbose_name=_("Endzeit"))
    nach_vereinbarung = models.BooleanField(default=False, verbose_name=_("Nach Vereinbarung"))

    def __str__(self):
        return f"{self.get_wochentag_display()} {self.startzeit} - {self.endzeit} {'(nach Vereinbarung)' if self.nach_vereinbarung else ''}"

    class Meta:
        verbose_name = _("Sprechzeit")
        verbose_name_plural = _("Sprechzeiten")


class PracticeClosure(models.Model):
    start_datum = models.DateField(verbose_name=_("Startdatum"))
    end_datum = models.DateField(verbose_name=_("Enddatum"))

    def __str__(self):
        return f"{self.start_datum} - {self.end_datum}"

    class Meta:
        verbose_name = _("Praxisschließzeit")
        verbose_name_plural = _("Praxisschließzeiten")
