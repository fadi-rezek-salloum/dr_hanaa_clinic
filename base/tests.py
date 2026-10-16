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

    def test_recaptcha_script_and_field_rendered(self):
        response = self.client.get(reverse("base:index"))
        content = response.content.decode("utf-8")
        if settings.RECAPTCHA_SITE_KEY:
            self.assertIn("https://www.google.com/recaptcha/api.js?render=", content)
            self.assertIn(settings.RECAPTCHA_SITE_KEY, content)
        self.assertIn('name="g-recaptcha-response"', content)
        self.assertIn('id="g-recaptcha-response"', content)

    def test_html_document_structure(self):
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
    def test_successful_submission_with_high_score(self, mock_thread, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({"success": True, "score": 0.9}).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        response = self.client.post(self.contact_url, data=self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Contact.objects.filter(email="max@example.com").exists())

    @patch("urllib.request.urlopen")
    @override_settings(DEBUG=False)
    def test_submission_blocked_in_production_when_score_low(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({"success": True, "score": 0.2}).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        response = self.client.post(self.contact_url, data=self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Contact.objects.filter(email="max@example.com").exists())

    @patch("urllib.request.urlopen")
    @override_settings(DEBUG=False)
    def test_submission_blocked_in_production_when_bot_detected(self, mock_urlopen):
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

    @patch("urllib.request.urlopen")
    @patch("threading.Thread.start")
    @override_settings(DEBUG=True)
    def test_submission_allowed_in_debug_mode_even_if_recaptcha_fails(self, mock_thread, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({"success": False, "score": 0.0}).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        response = self.client.post(self.contact_url, data=self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Contact.objects.filter(email="max@example.com").exists())

    @patch("urllib.request.urlopen")
    @patch("threading.Thread.start")
    @override_settings(DEBUG=False)
    def test_network_failure_fails_open_gracefully(self, mock_thread, mock_urlopen):
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
