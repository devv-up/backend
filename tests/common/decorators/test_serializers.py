import pytest
from common.decorators.serializers import serializer, filtered_serializer, required, field, Date, \
    model_serializer
from rest_framework import serializers

from tests.models import TestModel


@serializer(TestModel, {'test': 1})
class TestSerializer:
    test_str = required(str, 'test_str')
    test_date = field(Date, 'test_date')
    test_no_db = field(int, 'test_no_db', False)


@filtered_serializer(TestSerializer, ['test_str'])
class TestFilteredSerializer:
    test_int = required(int, 'test_int')


@model_serializer(TestModel, {'test': 1}, ['test_str'])
class TestModelSerializer:
    test_no_db = field(int, 'test_no_db', False)


@pytest.mark.django
def test_serializer():
    fields = TestSerializer._declared_fields
    assert isinstance(fields['test_str'], serializers.CharField)
    assert isinstance(fields['test_date'], serializers.DateField)
    assert isinstance(fields['test_no_db'], serializers.IntegerField)
    assert hasattr(TestSerializer, 'Meta')
    assert set(TestSerializer.Meta.fields) == {'test_str', 'test_date'}
    assert TestSerializer.Meta.model == TestModel
    assert TestSerializer.Meta.test == 1


@pytest.mark.django
def test_filtered_serializer():
    fields = TestFilteredSerializer._declared_fields
    assert isinstance(fields['test_int'], serializers.IntegerField)
    assert hasattr(TestFilteredSerializer, 'Meta')
    assert isinstance(fields['test_str'], serializers.CharField)
    assert fields.get('test_date', None) is None
    assert TestFilteredSerializer.Meta.model == TestModel
    assert set(TestFilteredSerializer.Meta.fields) == {'test_int', 'test_str'}


@pytest.mark.django
def test_model_serializer():
    fields = TestModelSerializer._declared_fields
    assert fields.get('test_int', None) is None
    assert fields.get('test_date', None) is None
    assert isinstance(fields['test_no_db'], serializers.IntegerField)
    assert hasattr(TestModelSerializer, 'Meta')
    assert TestModelSerializer.Meta.fields == tuple(['test_str'])
    assert TestModelSerializer.Meta.model == TestModel
    assert TestModelSerializer.Meta.test == 1
