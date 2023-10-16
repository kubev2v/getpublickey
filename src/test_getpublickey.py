import ssl
import unittest

from src import getpublickey


class TestGetServerCertificateInfo(unittest.TestCase):
    def test_get_certificate_info(self):
        # Use well known url
        url = "github.com"

        certificate_info = getpublickey.get_server_certificate_info(url)

        # Check if the returned certificate info dictionary has the expected keys
        self.assertIn("fingerprint", certificate_info)
        self.assertIn("certificate", certificate_info)

        # Check if the fingerprint is in the correct format
        self.assertRegex(
            certificate_info["fingerprint"], r"^([0-9a-fA-F]{2}:){19}[0-9a-fA-F]{2}$"
        )

        # Check if the certificate is in PEM format
        pem_certificate = certificate_info["certificate"]
        try:
            # Attempt to load the PEM certificate using OpenSSL to validate the format
            ssl.PEM_cert_to_DER_cert(pem_certificate)
        except ssl.SSLError:
            self.fail("Certificate is not in PEM format")

    def test_invalid_url(self):
        # Test with an invalid URL (should raise an exception)
        url = "invalid_url"
        certificate_info = getpublickey.get_server_certificate_info(url)

        self.assertIn("error", certificate_info)


if __name__ == "__main__":
    unittest.main()
