import pytest
from unittest.mock import patch

from click.exceptions import MissingParameter

from rfidsecuritysvc.cli.test import generate_api_key

@patch('rfidsecuritysvc.cli.test.generate_password_hash')
def test_generate_test_apikey_value(generate_password_hash, runner, assert_output):
    generate_password_hash.return_value = 'test'
    result = runner.invoke(args=['test', 'generate-test-apikey', 'test'])
    assert_output(result, 'test')
    generate_password_hash.assert_called_once_with('test')

def test_generate_test_apikey_value_required():
    with pytest.raises(MissingParameter, match='missing parameter: value'):
        generate_api_key.make_context('generate-api-key',[])

