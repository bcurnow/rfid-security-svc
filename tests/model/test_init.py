from rfidsecuritysvc.model import BaseModel

class ExampleModel(BaseModel):
    def __init__(self, test):
        self.test = test

def test_BaseModel_to_json():
    em = ExampleModel('tojson')
    assert em.to_json() == {'test': 'tojson'}

def test_BaseModel_str():
    em = ExampleModel('__str__')
    assert em.__str__() == str({'test': '__str__'})

def test_BaseModel_repr():
    em = ExampleModel('__repr__')
    assert em.__repr__() == str({'test': '__repr__'})
