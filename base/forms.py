import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Contact

# Matches any URL-like pattern bots typically paste.
_URL_PATTERN = re.compile(r"(https?://|www\.)", re.IGNORECASE)

# Matches any character in the Cyrillic Unicode block (U+0400–U+04FF).
_CYRILLIC_PATTERN = re.compile(r"[\u0400-\u04FF]")


def _check_spam(value: str, field_label: str) -> str:
    """Raise ValidationError if *value* contains URLs or Cyrillic characters."""
    if _URL_PATTERN.search(value):
        raise ValidationError(
            f"Das Feld \u201e{field_label}\u201c darf keine Links oder URLs enthalten."
        )
    if _CYRILLIC_PATTERN.search(value):
        raise ValidationError(
            f"Das Feld \u201e{field_label}\u201c enthält ungültige Zeichen."
        )
    return value


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["vorname", "name", "telefon", "email", "betreff", "nachricht"]
        widgets = {
            "vorname": forms.TextInput(attrs={"placeholder": "Vorname *", "required": True}),
            "name": forms.TextInput(attrs={"placeholder": "Name *", "required": True}),
            "telefon": forms.TextInput(attrs={"placeholder": "Telefon"}),
            "email": forms.EmailInput(attrs={"placeholder": "E-Mail *", "required": True}),
            "betreff": forms.TextInput(attrs={"placeholder": "Betreff *", "required": True}),
            "nachricht": forms.Textarea(
                attrs={"placeholder": "Nachricht *", "rows": "6", "required": True}
            ),
        }

    # ── Spam / content filters ────────────────────────────────────────────────

    def clean_vorname(self):
        return _check_spam(self.cleaned_data["vorname"], "Vorname")

    def clean_name(self):
        return _check_spam(self.cleaned_data["name"], "Name")

    def clean_betreff(self):
        return _check_spam(self.cleaned_data["betreff"], "Betreff")

    def clean_nachricht(self):
        return _check_spam(self.cleaned_data["nachricht"], "Nachricht")
