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
        with open(success_file, 'rb') as fp:
            response = self.client.post('/analyze/', {'file': fp})
            self.assertEqual(response.status_code, 200)

    def test_upload_failure_file_type(self):
        """
        Are we checking the types correctly?
        """
        upload_file = os.path.join(settings.STATIC_ROOT, "tests/file_type_fail_test.pdf")
        with open(upload_file, 'rb') as fp:
            response = self.client.post('/analyze/', {'file': fp})
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response.body, "Uploaded file must be an image.")
        upload_file = os.path.join(settings.STATIC_ROOT, "tests/image_type_fail_test.tiff")
        with open(upload_file, 'rb') as fp:
            response = self.client.post('/analyze/', {'file': fp})
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response.body, "Uploaded file must be an image of types jpeg, gif, png.")
