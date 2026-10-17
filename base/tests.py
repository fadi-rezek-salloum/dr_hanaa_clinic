import json
from unittest.mock import MagicMock, patch
from urllib.error import URLError

from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from base.models import Contact


class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_status_and_template(self):
        response = self.client.get(reverse("base:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/index.html")

    def test_recaptcha_v2_widget_rendered(self):
        """The .g-recaptcha div with the site key must appear in the form."""
        response = self.client.get(reverse("base:index"))
        content = response.content.decode("utf-8")
        if settings.RECAPTCHA_SITE_KEY:
            self.assertIn("class=\"g-recaptcha\"", content)
            self.assertIn(settings.RECAPTCHA_SITE_KEY, content)
            # v2 script (no ?render= param)
            self.assertIn(
                "https://www.google.com/recaptcha/api.js",
                content,
            )
            self.assertNotIn("?render=", content)

    def test_html_document_structure(self):
        """The page must end with </html> and the form must be inside the document."""
        response = self.client.get(reverse("base:index"))
        content = response.content.decode("utf-8").strip()
        self.assertTrue(content.endswith("</html>"))
        closing_html_pos = content.rfind("</html>")
        form_pos = content.find('id="contact-form"')
        self.assertNotEqual(form_pos, -1)
        self.assertLess(form_pos, closing_html_pos)


class ContactViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact_url = reverse("base:contact")
        self.valid_data = {
            "vorname": "Max",
            "name": "Mustermann",
            "email": "max@example.com",
            "telefon": "0123456789",
            "betreff": "Allgemeine Anfrage",
            "nachricht": "Guten Tag, dies ist eine Testnachricht.",
            "g-recaptcha-response": "fake-valid-token",
        }

    @patch("urllib.request.urlopen")
    @patch("threading.Thread.start")
    @override_settings(DEBUG=False)
    def test_successful_submission_when_recaptcha_passes(self, mock_thread, mock_urlopen):
        """Valid form + successful reCAPTCHA v2 → contact saved."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({"success": True}).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        response = self.client.post(self.contact_url, data=self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Contact.objects.filter(email="max@example.com").exists())

    @patch("urllib.request.urlopen")
    @override_settings(DEBUG=False)
    def test_blocked_in_production_when_bot_detected(self, mock_urlopen):
        """reCAPTCHA v2 returns success=False → form rejected in production."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({
            "success": False,
            "error-codes": ["invalid-input-response"],
        }).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        response = self.client.post(self.contact_url, data=self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Contact.objects.filter(email="max@example.com").exists())

    @override_settings(DEBUG=False)
    def test_blocked_in_production_when_no_token(self):
        """No reCAPTCHA token at all → rejected in production."""
        data = {**self.valid_data, "g-recaptcha-response": ""}
        response = self.client.post(self.contact_url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Contact.objects.filter(email="max@example.com").exists())

    @patch("urllib.request.urlopen")
    @patch("threading.Thread.start")
    @override_settings(DEBUG=True)
    def test_submission_allowed_in_debug_even_if_recaptcha_fails(self, mock_thread, mock_urlopen):
        """In DEBUG mode, a failed reCAPTCHA must not block the submission."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({"success": False}).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        response = self.client.post(self.contact_url, data=self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Contact.objects.filter(email="max@example.com").exists())

    @patch("urllib.request.urlopen")
    @patch("threading.Thread.start")
    @override_settings(DEBUG=False)
    def test_network_failure_fails_open_gracefully(self, mock_thread, mock_urlopen):
        """If Google's API is unreachable, the form should still go through."""
        mock_urlopen.side_effect = URLError("Temporary DNS error")

        response = self.client.post(self.contact_url, data=self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Contact.objects.filter(email="max@example.com").exists())


class StaticPagesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_datenschutz_page(self):
        response = self.client.get(reverse("base:datenschutz"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Google reCAPTCHA", response.content.decode("utf-8"))

    def test_impressum_page(self):
        response = self.client.get(reverse("base:impressum"))
        self.assertEqual(response.status_code, 200)

    def test_neupatienten_page(self):
        response = self.client.get(reverse("base:neupatienten"))
        self.assertEqual(response.status_code, 200)
