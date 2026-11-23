import unittest
import xml.etree.ElementTree as ET
from main import audit_tree

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

class SitemapTests(unittest.TestCase):
    def test_valid_urlset(self):
        root = ET.fromstring(f'<urlset xmlns="{NS}"><url><loc>https://example.org/</loc><lastmod>2026-01-01</lastmod></url></urlset>')
        report = audit_tree(root)
        self.assertEqual(report["findings"], [])

    def test_duplicate_locations_warn(self):
        root = ET.fromstring(f'<urlset xmlns="{NS}"><url><loc>https://example.org/</loc></url><url><loc>https://example.org/</loc></url></urlset>')
        report = audit_tree(root)
        self.assertTrue(any(x["level"] == "warning" for x in report["findings"]))

    def test_invalid_location_errors(self):
        root = ET.fromstring(f'<urlset xmlns="{NS}"><url><loc>/relative</loc></url></urlset>')
        report = audit_tree(root)
        self.assertTrue(any(x["level"] == "error" for x in report["findings"]))

if __name__ == "__main__":
    unittest.main()
