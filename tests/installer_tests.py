import unittest
import install_exporter as exporter


class InstallerTests(unittest.TestCase):

    def setUp(self):
        self.good_sha = 'e92a601a5ef4f77cce967266b488a978711dabc527a720bea26505cba426c029'
        self.bad_sha_1 = 'e92a601a5ef4f77cce967266b488a978711dabc527a720bea26505cba426c021'
        self.bad_sha_2 = 'abcdef'
        self.known_hash = '80ffbe9f24eb18cc9d4b843d6f50d28bd0228edb32f6051e19bbf4c36a286cfe'
        self.fail_cases = [
            [self.good_sha, self.bad_sha_1],
            [self.good_sha, self.bad_sha_2],
            [None, self.bad_sha_2],
            [self.good_sha, None],
            [self.good_sha, 10 ** 63],
            [self.good_sha, 10 ** 163],
            [self.good_sha, 10.13],
            [self.good_sha, ['a', 'b', 'c']],
            [self.good_sha, "!@#$%^&*\n()\t\b+<>?:;'\"'"],
        ]

    def test_sha_check(self):
        """Validate SHA check works"""

        self.assertTrue(exporter.validate_sha(sha=self.good_sha, return_hash=self.good_sha))

        for fail in self.fail_cases:
            self.assertFalse(exporter.validate_sha(sha=fail[0], return_hash=fail[1]))

    def test_checksum(self):
        """validate hashing"""
        self.assertEqual(exporter.get_checksum(file_name='./tests/known_hash_file'), self.known_hash)

        for fail in self.fail_cases:
            self.assertNotEqual(exporter.get_checksum(file_name='./tests/known_hash_file'), fail[1])
