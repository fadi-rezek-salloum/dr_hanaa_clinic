from django import forms

from .models import Contact


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
