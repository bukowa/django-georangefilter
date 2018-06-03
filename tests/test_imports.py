from django.test import SimpleTestCase


class PackageImportTestCase(SimpleTestCase):
    def test_can_import_package(self):
        import georangefilter
