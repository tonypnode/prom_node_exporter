import unittest
import install_exporter as exporter


class InstallerTests(unittest.TestCase):

    def setUp(self):
        self.good_sha = 'e92a601a5ef4f77cce967266b488a978711dabc527a720bea26505cba426c029'
        self.bad_sha_1 = 'abcdef'
        self.bad_sha_2 = 'e92a601a5ef4f77cce967266b488a978711dabc527a720bea26505cba426c021'

    def test_sha_check(self):
        """Validate SHA check works

        Test A sends known good SHAs - should return True
        Test B sends known BAD SHA - should return False
        Test C sends seconds known BAD SHA - should return False
        Test D/E sends None in either position - should return False
        Test F sends 64 len int - should return false
        Test G sends special chars - should return false

        """
        self.assertTrue(exporter.validate_sha(sha=self.good_sha, return_hash=self.good_sha))
        self.assertFalse(exporter.validate_sha(sha=self.good_sha, return_hash=self.bad_sha_1))
        self.assertFalse(exporter.validate_sha(sha=self.good_sha, return_hash=self.bad_sha_2))
        self.assertFalse(exporter.validate_sha(sha=None, return_hash=self.bad_sha_2))
        self.assertFalse(exporter.validate_sha(sha=self.good_sha, return_hash=None))
        self.assertFalse(exporter.validate_sha(sha=self.good_sha, return_hash=10**63))
        self.assertFalse(exporter.validate_sha(sha=self.good_sha, return_hash="!@#$%^&*\n()\t\b+<>?:;'\"'"))




