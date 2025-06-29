from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from staff.models import Staff
from timing.models import ConsultationTime, FreeAdmission, PracticeClosure

from .forms import ContactForm


class IndexView(TemplateView):
    template_name = "base/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["staff"] = Staff.objects.all().order_by("name")
        context["free_admissions"] = FreeAdmission.objects.all()
        context["consultation_times"] = ConsultationTime.objects.all()
        context["practice_closures"] = PracticeClosure.objects.all()
        return context


class ContactView(FormView):
    template_name = "base/index.html"
    form_class = ContactForm
    success_url = reverse_lazy("base:index")

    def form_valid(self, form):
        contact = form.save()

        html_message = render_to_string("_email.html", {"contact": contact})

        email = EmailMessage(
            subject="Vielen Dank für Ihre Anfrage",
            body=html_message,
            from_email="praxis@example.com",
            to=[contact.email],
        )
        email.content_subtype = "html"
        email.send()

        messages.success(
            self.request,
            "Vielen Dank für Ihre Nachricht! Eine Bestätigung wurde an Ihre E-Mail gesendet.",
        )
        return HttpResponseRedirect(f"{self.success_url}#contact")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
