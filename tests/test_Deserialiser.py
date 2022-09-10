"""Tests for deserialisers for converting strings to various formats."""
import pytest
from lib.core import DataFormat
from lib.services.io_service import Deserialiser


class TestGivenAnUndefinedDeserialiser:
    """Test operations for a serialiser without a defined format"""
    def test_empty_instantiation_will_throw(self):
        with pytest.raises(Exception) as e_info:
            Deserialiser()
        assert e_info.type == TypeError


class TestGivenAValidDeserialiserFormat:
    """Instantiation for correctly defined deserialisers"""
    def test_a_deserialiser_in_json_format_can_be_constructed(self):
        assert Deserialiser(DataFormat.JSON)


class TestGivenAnInvalidDeserialiserFormat:
    """Misidentified formats do not throw on instantiation, but when deserialise is called"""
    def test_deserialiser_will_throw_on_deserialise(self):
        with pytest.raises(Exception) as e_info:
            Deserialiser("ThisIsNotAFormat").deserialise('{"Any": "String}')
        assert e_info.type == KeyError


class Test_GivenADeserialiserInJSONFormat:
    """Operations for a deserialiser in JSON format"""
    def test_cm_ic_6_a_json_deserialise_method_is_called(self, mocker):
        """Calls to deserialise will call the JSON method"""
        # Behavioural test
        mock_deserialise = mocker.patch(
            "lib.services.io_service.JSONDeserialiser.deserialise",
            return_data={"A": "B", "C": 1})
        deserialiser = Deserialiser(DataFormat.JSON)
        teststring = '{"A": "B", "C": 1}'
        _ = deserialiser.deserialise(teststring)
        mock_deserialise.assert_called_once()

    def test_cm_ic_7_a_valid_string_will_deserialise(self):
        # State test
        # Integration Test: Deserialiser <- to/from -> JSON_Deserialiser
        json_deserialiser = Deserialiser(DataFormat.JSON)
        teststring = '{"A": "B", "C": 1}'
        deserialised_object = json_deserialiser.deserialise(teststring)
        assert deserialised_object == {"A": "B", "C": 1}

    def test_a_none_input_returns_an_empty_dict(self):
        # State test
        # Integration Test: Deserialiser <- to/from -> JSON_Deserialiser
        json_deserialiser = Deserialiser(DataFormat.JSON)
        teststring = None
        deserialised_object = json_deserialiser.deserialise(teststring)
        assert deserialised_object == dict()
