from django.db import models
from taggit.managers import TaggableManager


class Staff(models.Model):
    picture = models.ImageField(
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=120, blank=True, null=True)
    name = models.CharField(max_length=120)
    specialty = models.CharField(max_length=220)
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.name}"

    class Meta:
        verbose_name_plural = "Staff"
