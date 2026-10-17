import json
import logging
import threading
import urllib.parse
import urllib.request

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from django_ratelimit.decorators import ratelimit

from staff.models import Staff
from timing.models import ConsultationTime, FreeAdmission, PracticeClosure

from .forms import ContactForm

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "base/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["staff"] = Staff.objects.all().order_by("name").prefetch_related("tags")
        context["free_admissions"] = FreeAdmission.objects.all()
        context["consultation_times"] = ConsultationTime.objects.all()
        context["practice_closures"] = PracticeClosure.objects.all()
        return context


class ImpressumView(TemplateView):
    template_name = "base/impressum.html"


class DatenschutzView(TemplateView):
    template_name = "base/datenschutz.html"


class NeupatientenView(TemplateView):
    template_name = "base/neupatienten.html"


class ContactView(IndexView, FormView):
    template_name = "base/index.html"
    form_class = ContactForm
    success_url = reverse_lazy("base:index")

    def get_context_data(self, **kwargs):
        # Merge IndexView context (staff, schedules…) with FormView context (form)
        context = super().get_context_data(**kwargs)
        return context

    def _verify_recaptcha(self, token):
        """Verify a reCAPTCHA v2 token with Google's siteverify API.

        Returns True if the checkbox was successfully checked by a human.
        """
        secret = settings.RECAPTCHA_SECRET_KEY
        if not secret:
            logger.info("reCAPTCHA skipped: No secret key configured.")
            return True

        if not token:
            logger.warning("reCAPTCHA failed: No token received (user may not have checked the box).")
            return False

        data = urllib.parse.urlencode(
            {"secret": secret, "response": token}
        ).encode()
        req = urllib.request.Request(
            "https://www.google.com/recaptcha/api/siteverify",
            data=data,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            # In production, treat network failures as suspicious and reject.
            # In DEBUG, be lenient so local development still works.
            logger.warning("reCAPTCHA verification network error: %s", e)
            return settings.DEBUG

        success = result.get("success", False)
        error_codes = result.get("error-codes", [])

        if success:
            logger.info("reCAPTCHA v2 passed.")
        else:
            logger.warning("reCAPTCHA v2 failed: errors=%s", error_codes)

        return success

    @method_decorator(
        ratelimit(
            key="ip",
            rate=lambda g, r: getattr(settings, "CONTACT_RATELIMIT_RATE", "1/30m"),
            method="POST",
            block=False,
        )
    )
    def post(self, request, *args, **kwargs):
        # ── 1. Honeypot check (silent drop) ───────────────────────────────────
        if request.POST.get("hp_website", ""):
            logger.warning(
                "Honeypot triggered by IP %s – silently dropping submission.",
                request.META.get("REMOTE_ADDR"),
            )
            # Fake a success response so bots don't know they were caught.
            messages.success(
                request,
                "Vielen Dank für Ihre Nachricht! Eine Bestätigung wurde an Ihre E-Mail gesendet.",
            )
            return HttpResponseRedirect(f"{self.success_url}#contact")

        form = self.form_class(request.POST)

        # ── 2. Rate-limit check ────────────────────────────────────────────────
        if getattr(request, "limited", False):
            logger.warning(
                "Contact form submission blocked: rate limit exceeded for IP %s",
                request.META.get("REMOTE_ADDR"),
            )
            messages.error(
                request,
                "Sie haben vor kurzem bereits eine Nachricht gesendet. Bitte warten Sie 30 Minuten, bevor Sie eine weitere Nachricht senden.",
            )
            return self.form_invalid(form)

        # ── 3. Form validation (incl. spam-content checks in forms.py) ─────────
        if form.is_valid():
            # ── 4. reCAPTCHA v2 server-side verification ───────────────────────
            token = request.POST.get("g-recaptcha-response", "")
            ok = self._verify_recaptcha(token)
            if not ok:
                if settings.DEBUG:
                    logger.warning(
                        "DEBUG mode: reCAPTCHA check failed. "
                        "Bypassing rejection for local development."
                    )
                else:
                    messages.error(
                        request,
                        "Bitte bestätigen Sie, dass Sie kein Roboter sind.",
                    )
                    return self.form_invalid(form)
            return self.form_valid(form)
        return self.form_invalid(form)

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
        
        # Send email asynchronously to prevent blocking the request
        threading.Thread(target=email.send, kwargs={"fail_silently": True}).start()

        messages.success(
            self.request,
            "Vielen Dank für Ihre Nachricht! Eine Bestätigung wurde an Ihre E-Mail gesendet.",
        )
        return HttpResponseRedirect(f"{self.success_url}#contact")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
