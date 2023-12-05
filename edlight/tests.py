"""
Tests for the maths challenge
"""
import os
from django.conf import settings
from django.test import Client, TestCase


class ImageAnalysisTestCase(TestCase):
    """
    Testing that the analysis returns expected results

    """
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()

    def test_simple_image_upload(self):
        """
        can we access open ai at all?
        """
        success_file = os.path.join(settings.STATIC_ROOT, "tests/success_test.jpg")
        with open(success_file) as fp:
            self.client.post('/analyze', {'file': fp})
