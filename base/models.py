from django.db import models


class Contact(models.Model):
    vorname = models.CharField(max_length=100, verbose_name="Vorname")
    name = models.CharField(max_length=100, verbose_name="Name")
    telefon = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    email = models.EmailField(max_length=254, verbose_name="E-Mail")
    betreff = models.CharField(max_length=200, verbose_name="Betreff")
    nachricht = models.TextField(verbose_name="Nachricht")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Eingereicht am")

    def __str__(self):
        return f"{self.vorname} {self.name} - {self.betreff}"

    class Meta:
        verbose_name = "Kontakt"
        verbose_name_plural = "Kontakte"
