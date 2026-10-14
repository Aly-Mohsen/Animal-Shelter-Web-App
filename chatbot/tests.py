from django.test import TestCase
from django.test import SimpleTestCase
from rest_framework.test import APIClient


class ChatEndpointTests(SimpleTestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/chatbot/get-response/"

    def test_valid_message_returns_mock_reply(self):
        response = self.client.post(
            self.url,
            {"message": "Tell me about adoption"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"reply": "Mock reply to: 'Tell me about adoption'"},
        )

    def test_missing_message_is_rejected(self):
        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, 400)

    def test_whitespace_only_message_is_rejected(self):
        response = self.client.post(
            self.url,
            {"message": "   "},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_non_string_message_is_rejected(self):
        for message in (123, ["hello"], {"text": "hello"}):
            with self.subTest(message=message):
                response = self.client.post(
                    self.url,
                    {"message": message},
                    format="json",
                )

                self.assertEqual(response.status_code, 400)

    def test_message_over_limit_is_rejected(self):
        response = self.client.post(
            self.url,
            {"message": "a" * 2001},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_html_like_input_is_returned_as_data(self):
        message = "<img src=x onerror=alert(1)>"

        response = self.client.post(
            self.url,
            {"message": message},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["reply"],
            f"Mock reply to: '{message}'",
        )