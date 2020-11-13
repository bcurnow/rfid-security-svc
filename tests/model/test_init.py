from rfidsecuritysvc.model import BaseModel


class ExampleModel(BaseModel):
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2


    def _read_only_keys(self):
        return ['field2']


def test_BaseModel_to_json():
    em = ExampleModel('tojson', 'tojson2')
    assert em.to_json() == {'field1': 'tojson', 'field2': 'tojson2'}


def test_BaseModel_to_json_returns_copy_of_dict():
    em = ExampleModel('tojson', 'tojson2')
    assert em.field1 is not None
    d = em.to_json()
    d.pop('field1')
    assert em.field1 is not None


def test_BaseModel_to_json_rw():
    em = ExampleModel('field1', 'field2')
    assert em.to_json_rw() == {'field1': 'field1'}


def test_BaseModel_to_json_rw_returns_copy_of_dict():
    em = ExampleModel('tojson', 'tojson2')
    assert em.field1 is not None
    d = em.to_json_rw()
    d.pop('field1')
    assert em.field1 is not None


def test_BaseModel_str():
    em = ExampleModel('__str__', 'field2')
    assert em.__str__() == str({'field1': '__str__', 'field2': 'field2'})


def test_BaseModel_repr():
    em = ExampleModel('__repr__', 'field2')
    assert em.__repr__() == str({'field1': '__repr__', 'field2': 'field2'})
