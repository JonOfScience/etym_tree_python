"""Tests for serialisers for objects to strings in various formats."""
from enum import Enum
import pytest
from lib.core import DataFormat
from src.services.io_service import Serialiser


class TestGivenASerialiserWithInvalidSettings:
    """Test operations for a serialiser initialised with invalid format"""
    def test_empty_instantiation_will_throw(self):
        """A serialiser cannot exist without a specified format"""
        with pytest.raises(Exception) as e_info:
            Serialiser()  # pylint: disable=no-value-for-parameter
        assert e_info.type == TypeError

    def test_serialiser_will_throw_on_deserialise(self):
        """Serialiser will throw as it cannot find the format for the specified string"""
        class _NotAFormat(Enum):
            NOTAFORMAT = "NotAFormat"
        with pytest.raises(Exception) as e_info:
            Serialiser(_NotAFormat.NOTAFORMAT).serialise('{"Any": "String}')
        assert e_info.type == KeyError


class TestGivenAValidSerialiserFormat:
    """Instantiation for correctly defined serialisers"""
    def test_a_serialiser_in_json_format_can_be_constructed(self):
        """JSON is a recognised format"""
        assert Serialiser(DataFormat.JSON)


class TestGivenASerialiserInJSONFormat:
    """Operations for a serialiser in JSON format"""
    def test_serialise_produces_a_json_string(self):
        """Input dictionary object serialises to a JSON string"""
        json_serialiser = Serialiser(DataFormat.JSON)
        testobject = {"A": "B", "C": 1}
        serialised_string = json_serialiser.serialise(testobject)
        assert serialised_string == '{"A": "B", "C": 1}'
