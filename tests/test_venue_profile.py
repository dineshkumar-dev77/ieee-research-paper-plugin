import json
import os
import shutil
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/venue-profile/scripts"))
from venue_profile import DEFAULT_IEEE_CONFERENCE, validate_venue_schema, get_nested_param

class TestVenueProfile(unittest.TestCase):
    def test_default_ieee_conference_schema(self):
        valid, msg = validate_venue_schema(DEFAULT_IEEE_CONFERENCE)
        self.assertTrue(valid, msg)
        self.assertEqual(DEFAULT_IEEE_CONFERENCE["layout"]["single_column_width_in"], 3.5)
        self.assertEqual(DEFAULT_IEEE_CONFERENCE["captions"]["table_numbering"], "Roman")

    def test_get_nested_param(self):
        val = get_nested_param(DEFAULT_IEEE_CONFERENCE, "layout.single_column_width_in")
        self.assertEqual(val, 3.5)
        val_none = get_nested_param(DEFAULT_IEEE_CONFERENCE, "nonexistent.key")
        self.assertIsNone(val_none)

    def test_invalid_schema(self):
        bad_data = {"venue_id": "test"}
        valid, msg = validate_venue_schema(bad_data)
        self.assertFalse(valid)
